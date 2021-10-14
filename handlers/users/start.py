from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from filters import IsPrivate
from loader import dp

from utils.misc import rate_limit

# @dp.message_handler(CommandStart(deep_link="someDP"), IsPrivate())


@rate_limit()
@dp.message_handler(CommandStart(), IsPrivate())
async def bot_start(message: types.Message):
    await message.answer(f'Привет, {message.from_user.full_name}!')


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f'Приветствуем, {message.from_user.full_name} {message.from_user.id}!')
