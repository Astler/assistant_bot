from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

import re

positive_rep_keywords = [
    r"^\s*\+\s*$", r"\+rep", r"\+ rep", r"\+реп", r"\+ реп", r"плюс", r"плюсую", r"^\s*➕\s*$", r"^\s*❤\s*$"
]

negative_rep_keywords = [
    r"^\s*-\s*$", r"\-rep", r"\- rep", r"\-реп", r"\- реп", r"минус", r"минусую"
]

class ReputationFilter(BoundFilter):
    async def check(self, message: types.Message):
        text = message.text.lower()
        positive_rep = any(re.search(keyword, text) for keyword in positive_rep_keywords)
        negative_rep = any(re.search(keyword, text) for keyword in negative_rep_keywords)
        no_math_expression = not re.search(r"\d+(\+|\-)\d+", text)

        return (positive_rep or negative_rep) and no_math_expression
