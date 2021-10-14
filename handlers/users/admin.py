import asyncio

from aiogram import types
from aiogram.dispatcher.filters.builtin import AdminFilter

from filters import IsPrivate
from loader import dp


@dp.message_handler(IsPrivate(), AdminFilter(), commands=["id"])
async def bot_start(message: types.Message):
    await message.answer(f'Ваш id: {message.from_user.id}')
    await asyncio.sleep(1)
    await message.delete()
