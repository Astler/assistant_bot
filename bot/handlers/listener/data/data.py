import csv

import torch
from transformers import DistilBertForSequenceClassification, DistilBertTokenizerFast

from cat.utils.git_utils import push_git_data

advertisement = "Advertisement"
not_advertisement = "Not Advertisement"

label_names = [advertisement, not_advertisement]


async def add_new_data_to_ads_model(text: str, label: str):
    with open("labeled_messages.csv", mode="a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([text, label])

    with open("labeled_messages.csv", mode="r", encoding="utf-8", newline="") as f:
        push_git_data("labeled_messages.csv", f.read())

async def classify_message_by_model(text:str):
    loaded_model = DistilBertForSequenceClassification.from_pretrained("./trained_model")
    loaded_tokenizer = DistilBertTokenizerFast.from_pretrained("./trained_model")

    def classify(text):
        inputs = loaded_tokenizer(text, return_tensors="pt")
        outputs = loaded_model(**inputs)
        logits = outputs.logits
        probs = torch.softmax(logits, dim=-1)
        category_id = torch.argmax(probs).item()
        category = label_names[category_id]
        return category, probs[0].tolist()

    max_characters = 512

    def truncate_text(text, max_characters):
        return text[:max_characters]

    truncated_text = truncate_text(text, max_characters)

    return classify(truncated_text)