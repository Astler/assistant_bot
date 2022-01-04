from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class IsDotsMessage(BoundFilter):
    async def check(self, message: types.Message):
        return len(message.text.replace(".", "")) == 0 and message.from_user.id != 1072483718
