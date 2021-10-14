from aiogram import types
from loader import dp


@dp.message_handler()
async def spam_msg(message: types.Message):
    print(message.text)
    await message.edit_text("EDITED!")
    await message.answer("Ждём подтверждения ссылки администратором")
