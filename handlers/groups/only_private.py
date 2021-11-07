from aiogram import types

from filters import IsGroup
from loader import dp
from utils.misc import rate_limit
from utils.user_data.data import delete_simple_commands

@rate_limit()
@dp.message_handler(IsGroup(), commands=["sticker_id"])
@dp.message_handler(IsGroup(), commands=["id"])
async def get_my_id(message: types.Message):
    await message.bot.send_message(message.chat.id, "Эта команда срабоатет только в личных сообщениях")

    # TODO Обрабатывать данные для чата, а не конкретного пользователя
    if delete_simple_commands(message.from_user.id):
        await message.delete()

