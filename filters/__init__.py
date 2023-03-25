from aiogram import Dispatcher

from .is_group import IsGroup
from .cat_admin_filter import BotSuperAdminsFilter
from .private_chat import IsPrivate


def setup(dp: Dispatcher):
    pass
    dp.filters_factory.bind(IsGroup)
    dp.filters_factory.bind(IsPrivate)
    dp.filters_factory.bind(BotSuperAdminsFilter)
