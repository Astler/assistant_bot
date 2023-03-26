from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class IsDotsMessage(BoundFilter):
    async def check(self, message: types.Message):
        return message.text.replace(".", "") == ""
