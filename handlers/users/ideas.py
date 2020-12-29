from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import admins
from filters import IsGroup, IsPrivate
from loader import dp
from states import Idea
from utils.db_api.sqlite import Database

db = Database()
db.create_table_ideas()


@dp.message_handler(IsGroup(), commands="ideas_list", user_id=admins)
async def bot_echo(message: types.Message):
    await message.answer("За эти идеи отвечаю тут я! И покажу их только лично")


@dp.message_handler(commands="idea")
async def bot_echo(message: types.Message):
    await message.answer("Есть интересные мысли? Выкладывай! Боб запишет")
    await Idea.first()


@dp.message_handler(state=Idea.Q1)
async def answer_q1(message: types.Message, state: FSMContext):
    db.add_idea(message.text, message.from_user.full_name)
    await message.answer("Ты был услышан. Спасибо. Это всё?")
    await state.finish()


@dp.message_handler(commands="ideas_list", user_id=admins)
async def bot_echo(message: types.Message):
    await message.answer(f"Так. Сразу к делу. У нас в базе целых {db.count_ideas()[0]} идей! Смотрим все?")

    for idea in db.all_ideas():

        print(idea)
        await message.answer(f"Идея номер {idea[0]}\n\n{idea[1]}\n\nСтатус идеи: {idea[2]}\n\nАвтор: <b>{idea[4]}</b>")

    #Типо да


@dp.message_handler(commands="ideas_list")
async def bot_echo(message: types.Message):
    await message.answer("Нет! Обратись к старшему")
