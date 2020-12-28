from aiogram import types
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import ReplyKeyboardRemove

from keyboards.default import menu

from loader import dp


@dp.message_handler(Command("menu"))
async def show_menu(message: types.Message):
    await message.answer("Нашли ошибку? Желаете помочь? Есть идея?", reply_markup=menu)


@dp.message_handler(text="Ошибка/Сбой")
async def get_error_report(message: types.Message):
    await message.answer("О. Досадно. Не могли бы вы описать что конкретно произошло, когда, а лучше ещё и фото "
                         "загрузить?")


@dp.message_handler(text="Идея")
async def get_idea(message: types.Message):
    await message.answer("Буду рад услышать все ваши идеи!")


@dp.message_handler(Text(equals=["Помощь"]))
async def get_help(message: types.Message):
    await message.answer("Любая помощь будет полезна!", reply_markup=ReplyKeyboardRemove())
