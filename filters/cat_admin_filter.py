from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from utils.admin_data.data import get_a_list


class BotSuperAdminsFilter(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return get_a_list().__contains__(message.from_user.id)
