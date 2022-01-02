from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class IsRepMsg(BoundFilter):
    async def check(self, message: types.Message):
        return message.text.__contains__("+rep") or message.text.__contains__("-rep") or message.text.__contains__(
            "+реп") or message.text.__contains__("-реп")
