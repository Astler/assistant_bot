from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("help", "Помощь"),
        types.BotCommand("my_rep", "Ваша репутация (в текущем чате)"),
        types.BotCommand("settings", "Настройки"),
        # types.BotCommand("ro", "Мут пользователя. Первый параметр - причина, а второй - время в минутах"),
    ])
