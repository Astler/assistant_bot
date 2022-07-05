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
        text = message.text.lower()
        return any(word in text for word in positive_rep) or any(
            word in text for word in negative_rep) or text == "+" or text == "-" or text == "➕" or text == "❤"
