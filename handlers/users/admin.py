from aiogram import types

from loader import dp
from filters import IsPrivate

from data.config import admins


@dp.message_handler(IsPrivate(), commands="secret", user_id=admins)
async def bot_echo(message: types.Message):
    await message.answer("Вы имеете доступ к секретному разделу!")


@dp.message_handler(commands="secret", user_id=admins)
async def bot_echo(message: types.Message):
    await message.answer("Вы имеете доступ к секретному разделу!")


@dp.message_handler(text="лепи")
async def bot_wtf(message: types.Message):
    await message.answer("Леха пидор!")
