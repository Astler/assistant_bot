from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp
from utils.misc import rate_limit


@rate_limit(5, 'help')
@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = [
        'Список команд: ',
        '/start - Начать диалог',
        '/help - Получить справку',
        '/menu - Нашли ошибку? Желаете помочь? Есть идея?',
        '/mlv - Последняя вресия игры',
        '/hof - Зал славы сообщества KB',
        '/links - Полезные ссылки',
        '/tester - Инструкция как получать регулярные тестовые версии через App Tester'
    ]
    await message.answer('\n'.join(text))
