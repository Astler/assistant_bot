from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("help", "Помощь"),
        types.BotCommand("print_fool", "Для Даши, плохой код"),
        types.BotCommand("print_good", "Для Даши, уже лучше код"),
    ])
