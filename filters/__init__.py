from aiogram import Dispatcher

from .admin_filter import AdminFilter
from .is_group import IsGroup
from .private_chat import IsPrivate


def setup(dp: Dispatcher):
    pass
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(IsGroup)
