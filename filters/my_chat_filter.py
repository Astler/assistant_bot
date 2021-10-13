from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from data.config import chats


class MyChatFilter(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return chats.__contains__(message.chat.id)
