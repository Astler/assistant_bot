from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from data.dev.data import is_sa


class BotSuperAdminsFilter(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return is_sa(message.from_user.id)
