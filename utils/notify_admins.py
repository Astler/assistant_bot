import logging

from aiogram import Dispatcher

from data.config import admins, version


async def on_startup_notify(dp: Dispatcher):
    for admin in admins:
        try:
            await dp.bot.send_message(admin, f"Бот Запущен и готов к работе v{version}")
        except Exception as err:
            logging.exception(err)
