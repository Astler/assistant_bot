from aiogram import types
from aiogram.dispatcher.filters import AdminFilter

from bot.filters import IsGroup
from loader import dp


@dp.message_handler(IsGroup(), AdminFilter(), commands=["chat_id"])
async def get_chat_id(message: types.Message):
    await message.delete()
    await message.answer(message.chat.id)
