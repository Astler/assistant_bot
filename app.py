import os

from aiogram.utils.executor import start_webhook

from utils.set_bot_commands import set_default_commands
from loader import bot, dp
import logging

from data.config import (WEBHOOK_URL, WEBHOOK_PATH,
                         WEBAPP_HOST, WEBAPP_PORT)


async def on_startup(dp):
    await bot.delete_webhook()
    await bot.set_webhook(WEBHOOK_URL)

    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)
    logging.info(dp)

    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)
    await set_default_commands(dp)


async def on_shutdown(dp):
    logging.warning("Shutting down..")
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning("Bot down")


if __name__ == '__main__':
    from aiogram import executor, types
    from handlers import dp

    path = os.getcwd() + "/users/"

    try:
        os.makedirs(path)
    except OSError:
        print("Creation of the directory %s failed" % path)
    else:
        print("Successfully created the directory %s " % path)

    if "HEROKU" in list(os.environ.keys()):
        start_webhook(dispatcher=dp, webhook_path=WEBHOOK_PATH,
                      on_startup=on_startup, on_shutdown=on_shutdown,
                      host=WEBAPP_HOST, port=WEBAPP_PORT)
    else:
        executor.start_polling(dispatcher=dp,
                               on_startup=on_startup, on_shutdown=on_shutdown, )
