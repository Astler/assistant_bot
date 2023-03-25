import asyncio
from enum import Enum

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ParseMode
from aiogram.utils.markdown import escape_md

from cat.utils.files_utils import save_local_file
from cat.utils.ftp_utils import upload_file_to_folder
from cat.utils.json_utils import generate_json_string
from data.config import HOF_FILE
from filters import IsPrivate, BotAdminsFilter
from loader import dp, bot
from utils.hof.hof_utils import load_hof_array, HOFItem, encode_hof
from utils.misc import rate_limit


class HofEditingKeys(Enum):
    hof_array = 1
    request_id = 2
    remove_item_message_id = 3
    new_item_message_id = 4
    entered_name = 5


class DataState(StatesGroup):
    actionWait = State()
    enterName = State()
    enterDescription = State()
    enterItemToRemove = State()


def create_hof_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton("Add Item", callback_data="add_item"),
        types.InlineKeyboardButton("Remove Item", callback_data="remove_item"),
        types.InlineKeyboardButton("Publish", callback_data="publish"),
        types.InlineKeyboardButton("Finish", callback_data="finish"),
    ]
    keyboard.add(*buttons)
    return keyboard


async def update_hof_message(hof_list: list, chat_id: int, message_id: int):
    output_msg = [f"*{escape_md(item.name)}*\n{escape_md(item.description)}" for item in hof_list]
    data_from_server = "\n\n".join(output_msg)

    await bot.edit_message_text(text=f"Спасибо всем, кто помогал и продолжает помогать!\n\n{data_from_server}",
                                chat_id=chat_id,
                                message_id=message_id,
                                parse_mode=ParseMode.MARKDOWN,
                                reply_markup=create_hof_keyboard())


async def self_destroy_reply(original_message: types.Message, message_text: str, delete_original: bool = True):
    time_to_delete = 3

    hint_message = await original_message.reply(message_text + f"\n\nWill be deleted in {time_to_delete}")

    for i in range(1, time_to_delete + 1):
        await asyncio.sleep(1)
        await hint_message.edit_text(message_text + f"\n\nWill be deleted in {time_to_delete - i}")

    if delete_original:
        await original_message.delete()

    await hint_message.delete()


@rate_limit()
@dp.message_handler(IsPrivate(), BotAdminsFilter(), commands="update_hof_versions")
async def bot_start(message: types.Message, state: FSMContext):
    msg = await bot.send_message(message.chat.id, "Начинаю загрузку данных HOF...")

    result = load_hof_array()

    if not isinstance(result, list):
        await message.reply(result)
        return

    await update_hof_message(result, msg.chat.id, msg.message_id)

    async with state.proxy() as data:
        data[HofEditingKeys.hof_array] = result
        data[HofEditingKeys.request_id] = msg.message_id

    await DataState.actionWait.set()


@dp.callback_query_handler(lambda call: call.data == 'finish', state=DataState.actionWait)
async def cancel(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        message_id = data[HofEditingKeys.request_id]

    chat_id = call.message.chat.id
    await bot.delete_message(chat_id=chat_id, message_id=message_id)
    await bot.send_message(chat_id=chat_id, text="Operation finished")
    await call.answer()
    await state.finish()


@dp.callback_query_handler(lambda call: call.data == 'add_item', state=DataState.actionWait)
async def start_adding_item(call: types.CallbackQuery, state: FSMContext):
    await call.answer("New item!")

    message = await bot.send_message(text="Please enter the name of the item to remove.", chat_id=call.message.chat.id)

    async with state.proxy() as data:
        data[HofEditingKeys.new_item_message_id] = message.message_id

    await DataState.enterName.set()


@dp.message_handler(lambda message: not message.text.startswith('/'), state=DataState.enterName)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text

    async with state.proxy() as data:
        data[HofEditingKeys.entered_name] = name
        new_item_message_id = data[HofEditingKeys.new_item_message_id]

    await message.delete()
    await bot.edit_message_text(text=f"Name: {name}\n\nPlease enter the description of the new item.",
                                message_id=new_item_message_id,
                                chat_id=message.chat.id)
    await DataState.enterDescription.set()


@dp.message_handler(lambda message: not message.text.startswith('/'), state=DataState.enterDescription)
async def process_description(message: types.Message, state: FSMContext):
    description = message.text

    async with state.proxy() as data:
        name = data[HofEditingKeys.entered_name]
        message_id = data[HofEditingKeys.request_id]
        hof_array = data[HofEditingKeys.hof_array]
        new_item_message_id = data[HofEditingKeys.new_item_message_id]

    hof_item = HOFItem(name, description)

    async with state.proxy() as data:
        hof_array.append(hof_item)
        data[HofEditingKeys.hof_array] = hof_array

    await message.delete()
    result_message = await bot.edit_message_text(text=f"Item added.\n\nName: {name}\nDescription: {description}",
                                                 message_id=new_item_message_id,
                                                 chat_id=message.chat.id)

    await update_hof_message(hof_array, message.chat.id, message_id)

    await DataState.actionWait.set()

    await asyncio.sleep(1)
    await result_message.delete()


@dp.callback_query_handler(lambda call: call.data == 'remove_item', state=DataState.actionWait)
async def start_removing_item(call: types.CallbackQuery, state: FSMContext):
    remove_item_message = await bot.send_message(text="Please enter the name to remove.",
                                                 chat_id=call.message.chat.id)

    async with state.proxy() as data:
        data[HofEditingKeys.remove_item_message_id] = remove_item_message.message_id

    await DataState.enterItemToRemove.set()


@dp.message_handler(lambda message: not message.text.startswith('/'), state=DataState.enterItemToRemove)
async def process_item_to_remove(message: types.Message, state: FSMContext):
    item_name = message.text

    await message.delete()

    async with state.proxy() as data:
        hof_array = data[HofEditingKeys.hof_array]
        message_id = data[HofEditingKeys.request_id]
        remove_item_message_id = data[HofEditingKeys.remove_item_message_id]

    item_to_remove = None

    for item in hof_array:
        if item.name.lower() == item_name.lower():
            item_to_remove = item
            break

    if item_to_remove:
        hof_array.remove(item_to_remove)
        async with state.proxy() as data:
            data[HofEditingKeys.hof_array] = hof_array

        updated_text = f"Item '{item_name}' removed."
    else:
        updated_text = f"Item '{item_name}' not found."

    await bot.edit_message_text(text=updated_text, message_id=remove_item_message_id,
                                chat_id=message.chat.id)

    await update_hof_message(hof_array, message.chat.id, message_id)
    await DataState.actionWait.set()


@dp.message_handler(state=DataState.actionWait)
async def process_text_input(message: types.Message, state: FSMContext):
    hint_text = f"Incorrect input {message.text}\n\nPlease use the buttons to add or remove items. Or finish."
    await self_destroy_reply(message, hint_text)


@dp.callback_query_handler(lambda call: call.data == 'publish', state=DataState.actionWait)
async def start_removing_item(call: types.CallbackQuery, state: FSMContext):
    remove_item_message = await bot.send_message(text="Uploading data to server...", chat_id=call.message.chat.id)

    await call.answer()

    async with state.proxy() as data:
        hof_array = data[HofEditingKeys.hof_array]

    try:
        save_local_file(HOF_FILE, generate_json_string(hof_array, encode_hof))
        upload_file_to_folder(HOF_FILE)

        await remove_item_message.edit_text(f"Succeed!\n")
    except Exception as e:
        await remove_item_message.edit_text(f"Failed with error {e}!\n")

    await state.finish()
