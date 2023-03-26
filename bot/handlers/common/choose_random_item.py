import random

from aiogram import types

from data.config import BOT_NAMES
from bot.filters.random_item_filter import RandomItemFilter
from loader import dp


import re

@dp.message_handler(RandomItemFilter())
async def bot_choose(message: types.Message):
    msg_text = str(message.text).replace("?", "")

    pattern = r'^\s*(?:' + '|'.join(re.escape(name) for name in BOT_NAMES) + r')\s*,?\s*'
    msg_text = re.sub(pattern, '', msg_text, flags=re.IGNORECASE)

    variants = re.split(r'\s+или\s+', msg_text.strip())

    await message.reply(f"{random.choice(variants)}")
