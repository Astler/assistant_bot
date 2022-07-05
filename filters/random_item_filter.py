from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class RandomItemFilter(BoundFilter):
    async def check(self, message: types.Message):
        return message.text.lower().startswith("эш") and message.text.lower().__contains__(" или ")
