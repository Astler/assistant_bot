from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from filters import IsPrivate
from loader import dp
from utils.misc import rate_limit


@rate_limit()
@dp.message_handler(CommandHelp(), IsPrivate())
async def bot_help(message: types.Message):
    text = [
        '/sticker_id - бот вернет айди всех отправленных стикеров',
        '/id - бот вернет ваш id в Telegram',
    ]
    await message.answer('\n'.join(text))
