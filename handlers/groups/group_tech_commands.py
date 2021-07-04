from aiogram import types

from filters import IsGroup
from filters.admin_filter import AdminFilter
from loader import dp


@dp.message_handler(IsGroup(), AdminFilter(), commands=["chat_id"])
async def get_chat_id(message: types.Message):
    await message.delete()
    await message.answer(message.chat.id)
    print(message.chat.id)
