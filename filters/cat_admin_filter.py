from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from data.config import admins


class CATAdminsFilter(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return admins.__contains__(message.from_user.id)
