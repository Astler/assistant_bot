from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from data.config import BOT_NAMES


class ChooseItemFilter(BoundFilter):
    async def check(self, message: types.Message):
        possible_names = (name.lower() for name in BOT_NAMES)
        message_text = message.text.lower()
        return any(name in message_text for name in possible_names) and "кто сегодня" in message_text
