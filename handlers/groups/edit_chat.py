import io

from aiogram import types
from aiogram.dispatcher.filters import Command

from filters import IsGroup
from filters.admin_filter import AdminFilter
from loader import dp, bot


@dp.message_handler(IsGroup(), Command("set_photo", prefixes="!/"), AdminFilter())
async def set_chat_photo(message: types.Message):
    source_message = message.reply_to_message
    photo = source_message.photo[-1]
    photo = await photo.download(destination=io.BytesIO())
    input_files = types.InputFile(path_or_bytesio=photo)
    await bot.set_chat_photo(chat_id=message.chat.id, photo=input_files)


@dp.message_handler(IsGroup(), Command("set_title", prefixes="!/"), AdminFilter())
async def set_chat_photo(message: types.Message):
    source_message = message.reply_to_message
    title = source_message.text
    await bot.set_chat_title(title)


@dp.message_handler(IsGroup(), Command("set_description", prefixes="!/"), AdminFilter())
async def set_chat_photo(message: types.Message):
    source_message = message.reply_to_message
    title = source_message.text
    await bot.set_chat_description(title)

