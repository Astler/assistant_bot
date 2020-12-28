import os

from utils.set_bot_commands import set_default_commands
from loader import bot, dp
import logging
from aiogram import types
from aiogram.dispatcher.webhook import get_new_configured_app

from data.config import (BOT_TOKEN, HEROKU_APP_NAME,
                         WEBHOOK_URL, WEBHOOK_PATH,
                         WEBAPP_HOST, WEBAPP_PORT)


async def on_startup(dp):
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)

    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)
    await set_default_commands(dp)

    await bot.delete_webhook()
    await bot.set_webhook(WEBHOOK_URL)


# Run before shutdown
async def on_shutdown(dp):
    logging.warning("Shutting down..")
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning("Bot down")


if __name__ == '__main__':
    from aiogram import executor, types
    from handlers import dp

    if "HEROKU" in list(os.environ.keys()):
        executor.start_webhook(
            dispatcher=dp,
            webhook_path=WEBHOOK_PATH,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            host=WEBAPP_HOST,
            port=WEBAPP_PORT,
        )
    else:
        executor.start_polling(dp)
