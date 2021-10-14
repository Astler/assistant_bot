from aiogram import Dispatcher

from .is_group import IsGroup
from .private_chat import IsPrivate


def setup(dp: Dispatcher):
    pass
    dp.filters_factory.bind(IsGroup)
