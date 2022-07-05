from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from filters import IsGroup
from loader import dp


@dp.message_handler(CommandStart(), IsGroup())
async def bot_start(message: types.Message):
    await message.answer(f'Я уже тут, в чате {message.chat.full_name}!')
