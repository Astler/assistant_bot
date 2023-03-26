from aiogram import types

from bot.filters import IsGroup
from loader import dp
from utils.group_data.data import get_group_info
from utils.misc import rate_limit


@rate_limit()
@dp.message_handler(IsGroup(), commands=["id", "add_channel", "sticker_id"])
async def get_my_id(message: types.Message):
    await message.answer(f"Команда \"{message.text}\" срабоатет только в личных сообщениях!")

    chat_id = message.chat.id
    group_info = get_group_info(chat_id)

    if group_info.delete_commands:
        await message.delete()
