from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from data.config import BOT_NAMES


class RandomItemFilter(BoundFilter):
    async def check(self, message: types.Message):
        possible_names = (name.lower() for name in BOT_NAMES)
        message_text = message.text.lower()
        return any(message_text.startswith(name) for name in possible_names) and message_text.__contains__(" или ")
