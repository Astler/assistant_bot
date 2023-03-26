import asyncio
import datetime
import logging
import os

import aioschedule as aioschedule

from bot.listener.listener import try_to_start_listener
from loader import bot
from utils.minecraft.be_version_updater import be_version_push, be_version_get
from utils.set_bot_commands import set_default_commands


async def on_startup(dp):
    import bot.filters
    import middlewares
    bot.filters.setup(dp)
    middlewares.setup(dp)
    logging.info(dp)

    await try_to_start_listener()
    await be_version_push(await be_version_get())

    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)
    await set_default_commands(dp)

    asyncio.ensure_future(scheduler_combined())


async def combined_task():
    now = datetime.datetime.now()
    if now.minute == 0:
        await be_version_push(await be_version_get())


async def scheduler_combined():
    aioschedule.every().minute.do(combined_task)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_shutdown(dp):
    logging.warning("Shutting down..")
    from utils.notify_admins import on_shutdown_notify
    await on_shutdown_notify(dp)

    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning("Bot down")


if __name__ == '__main__':
    from aiogram import executor

    # new!
    from bot import dp

    # old!
    from handlers import dp

    path = os.getcwd() + "/users/"

    try:
        os.makedirs(path)
    except OSError:
        print("Creation of the directory %s failed" % path)
    else:
        print("Successfully created the directory %s " % path)

    # app.start()

    executor.start_polling(dispatcher=dp, on_startup=on_startup, on_shutdown=on_shutdown)
