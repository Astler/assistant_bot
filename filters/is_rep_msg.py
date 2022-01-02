from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

positive_rep = [
    "+rep",
    "+ rep",
    "+реп",
    "+ реп",
]

negative_rep = [
    "-rep",
    "- rep",
    "-реп",
    "- реп",
]


class IsRepMsg(BoundFilter):
    async def check(self, message: types.Message):
        return any(word in message.text for word in positive_rep) or any(word in message.text for word in negative_rep)
