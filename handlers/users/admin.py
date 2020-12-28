from aiogram import types

from data.config import admins
from filters import IsGroup
from loader import dp


@dp.message_handler(IsGroup(), commands="secret", user_id=admins)
async def bot_echo(message: types.Message):
    await message.answer("Хочешь обсудить секреты в публичном месте? Именно поэтому главная тут я! Нет.")


@dp.message_handler(commands="secret", user_id=admins)
async def bot_echo(message: types.Message):
    await message.answer("Похоже, что ты попал в список расширенного доступа. Поздравляю!")


@dp.message_handler(commands="secret")
async def bot_echo(message: types.Message):
    await message.answer("Доступ закрыт!")
