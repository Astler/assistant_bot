from aiogram import Dispatcher

from .throttling import ThrottlingMiddleware
from .database import GetDBUser


def setup(dp: Dispatcher):
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(GetDBUser())
