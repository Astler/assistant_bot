from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class IsDotsMessage(BoundFilter):
    async def check(self, message: types.Message):
        return len(message.text.replace(".", "")) == 0
