import logging

from aiogram import Dispatcher
from data.config import admins, version


async def on_startup_notify(dp: Dispatcher):
    await send_msg_to_admin(dp, f"Бот Запущен и готов к работе v{version}!")


async def on_shutdown_notify(dp: Dispatcher):
    await send_msg_to_admin(dp, "Работа бота завершена!")


async def send_msg_to_admin(dp: Dispatcher, msg: str):
    for admin in admins:
        try:
            await dp.bot.send_message(admin, msg)
        except Exception as err:
            logging.exception(err)
