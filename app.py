import os

from aiogram.utils.executor import start_webhook

from utils.set_bot_commands import set_default_commands
from loader import bot, dp
import logging
from aiogram import types, md
from aiogram.dispatcher.webhook import get_new_configured_app

from data.config import (BOT_TOKEN, HEROKU_APP_NAME,
                         WEBHOOK_URL, WEBHOOK_PATH,
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



# Run before shutdown
async def on_shutdown(dp):
    logging.warning("Shutting down..")
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning("Bot down")


@dp.message_handler(commands='start')
async def welcome(message: types.Message):
    await bot.send_message(
        message.chat.id,
        f'Приветствую! Это демонтрационный бот\n'
        f'Подробная информация на '
        f'{md.hlink("github", "https://github.com/deploy-your-bot-everywhere/heroku")}',
        parse_mode=types.ParseMode.HTML,
        disable_web_page_preview=True)


@dp.message_handler()
async def echo(message: types.Message):
    await bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    from aiogram import executor, types
    from handlers import dp

    start_webhook(dispatcher=dp, webhook_path=WEBHOOK_PATH,
                  on_startup=on_startup, on_shutdown=on_shutdown,
                  host=WEBAPP_HOST, port=WEBAPP_PORT)


# if "HEROKU" in list(os.environ.keys()):
# else:
#     executor.start_polling(dp)

