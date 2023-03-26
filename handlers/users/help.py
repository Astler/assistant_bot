from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from bot.filters import IsPrivate
from loader import dp
from utils.misc import rate_limit


@rate_limit()
@dp.message_handler(CommandHelp(), IsPrivate())
async def bot_help(message: types.Message):
    text = [
        '/id - бот вернет ваш id в Telegram'
        '/sticker_id - бот вернет айди всех отправленных стикеров',
        '/add_channel - добавить свой канал для публикации постов/редактирования (в разработке!)',
        '/my_channels - список ваших каналов',
        '/profile - настройки поведения бота и заданные параметры',
        '/profile true/false - включение/отключение очистки команд',
    ]
    await message.answer('\n'.join(text))
