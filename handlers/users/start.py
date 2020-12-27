from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from filters import IsPrivate
from loader import dp, bot
from utils.misc import rate_limit
from utils.db_api.user import User


@dp.message_handler(CommandStart(deep_link="faggot"), IsPrivate())
async def bot_start(message: types.Message):
    await message.answer(f'Хмм, похоже тебе дали особую ссылку, {message.from_user.full_name}!\nИ у меня для тебя '
                         f'особое сообщение :D\n\n{message.from_user.first_name}, ты козёл!')


# @rate_limit(limit=10)
@dp.message_handler(CommandStart(), IsPrivate())
async def bot_start(message: types.Message, user: User):
    await message.answer(f'Привет, {message.from_user.full_name}!')
    await message.answer(f'Твои данные из базы данных:\n{user.__dict__}!')


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f'Приветствуем, {message.from_user.full_name} {message.from_user.id}!')
