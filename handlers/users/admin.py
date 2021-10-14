import asyncio

from aiogram import types

from filters import IsPrivate
from filters.cat_admin_filter import CATAdminsFilter
from loader import dp


@dp.message_handler(IsPrivate(), CATAdminsFilter(), commands=["id"])
async def bot_start(message: types.Message):
    await message.answer(f'Ваш id: {message.from_user.id}')
    await asyncio.sleep(1)
    await message.delete()
