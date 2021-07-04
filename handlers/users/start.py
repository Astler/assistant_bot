from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from filters import IsPrivate
from loader import dp
from utils.db_api.sqlite import Database

db = Database()
db.create_table_users()


@dp.message_handler(CommandStart(deep_link="faggot"), IsPrivate())
async def bot_start(message: types.Message):
    await message.answer(f'Хмм, похоже тебе дали особую ссылку, {message.from_user.full_name}!\nИ у меня для тебя '
                         f'особое сообщение :D\n\n{message.from_user.first_name}, ты козёл!')


# @rate_limit(limit=10)
@dp.message_handler(CommandStart(), IsPrivate())
async def bot_start(message: types.Message):
    await message.answer(f'Привет, {message.from_user.full_name}!')
    user = db.get_user_data_by_id(message.from_user.id)

    if len(user) != 0:
        await message.answer(f'Твои данные из базы данных:\n{user}!')
    else:
        print("No Such User! ")


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f'Приветствуем, {message.from_user.full_name} {message.from_user.id}!')
