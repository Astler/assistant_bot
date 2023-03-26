from aiogram import types

from filters import IsPrivate
from loader import dp
from utils.misc import rate_limit
from utils.user_data.data import delete_simple_commands


@rate_limit()
@dp.message_handler(IsPrivate(), commands=["id"])
async def get_my_id(message: types.Message):
    await message.answer(f'Ваш id: {message.from_user.id}')

    if delete_simple_commands(message.from_user.id):
        await message.delete()
