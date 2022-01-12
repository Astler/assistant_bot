import random

from aiogram import types

from filters.choose_item_msg_filter import ChooseItemFilter
from loader import dp


@dp.message_handler(ChooseItemFilter())
async def bot_choose(message: types.Message):
    msg_text = str(message.text).replace("?", "")[2:].strip()

    if msg_text.startswith(","):
        msg_text = msg_text[1:]

    variants = msg_text.strip().split("или")

    await message.reply(f"{random.choice(variants)}")
