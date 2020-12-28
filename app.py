from utils.set_bot_commands import set_default_commands
from loader import bot, dp
import logging
from aiogram import types
from aiogram.utils.executor import start_webhook
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

    logging.warning(
        'Starting connection. ')
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


if __name__ == '__main__':
    from aiogram import executor, types
    from handlers import dp

    executor.start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )

    #executor.start_polling(dp, on_startup=on_startup)
