from aiogram import types
from datasets import load_dataset
from transformers import DistilBertTokenizerFast

from bot.handlers.listener.data.data import advertisement, not_advertisement, label_names
from filters import BotSuperAdminsFilter
from loader import dp

model_id = "distilbert-base-multilingual-cased"

@dp.message_handler(BotSuperAdminsFilter(), commands=['train'])
async def cmd_add_to_listener(message: types.Message):
    dataset = load_dataset("csv", data_files={"train": "labeled_messages.csv"})

    print(dataset.values())

    labels_map = {
        advertisement: 0,
        not_advertisement: 1,
    }

    dataset = dataset['train'].train_test_split(train_size=0.8, test_size=0.2)

    tokenizer = DistilBertTokenizerFast.from_pretrained(model_id)

    def tokenize_function(examples):
        return tokenizer(examples["message"], padding="max_length", truncation=True)

    tokenized_dataset = dataset.map(tokenize_function, batched=True)

    def encode_labels(example):
        print("Example:", example)
        example["label"] = int(labels_map[example["label"]])
        return example

    # Apply the encode_labels function to the dataset
    encoded_dataset = tokenized_dataset.map(encode_labels)

    from transformers import DistilBertForSequenceClassification, Trainer, TrainingArguments

    model = DistilBertForSequenceClassification.from_pretrained(model_id, num_labels=len(label_names))

    training_args = TrainingArguments(
        output_dir="./results",
        num_train_epochs=3,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        evaluation_strategy="epoch",
        logging_dir="./logs",
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=encoded_dataset["train"],
        eval_dataset=encoded_dataset["test"],
    )

    trainer.train()

    model.save_pretrained("./trained_model")
    tokenizer.save_pretrained("./trained_model")
