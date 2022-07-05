from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

positive_rep = [
    "+rep",
    "+ rep",
    "+реп",
    "+ реп",
    "плюс",
    "плюсую",
]

negative_rep = [
    "-rep",
    "- rep",
    "-реп",
    "- реп",
    "минус",
    "минусую",
]


class IsRepMsg(BoundFilter):
    async def check(self, message: types.Message):
        return any(word in message.text for word in positive_rep) or any(
            word in message.text for word in negative_rep) or str(message.text) == "+" or str(
            message.text) == "-" or str(message.text) == "➕" or str(message.text) == "❤"
