from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from filters import IsPrivate, BotAdminsFilter
from loader import dp
from utils.misc import rate_limit


@rate_limit()
@dp.message_handler(CommandHelp(), IsPrivate(), BotAdminsFilter())
async def bot_help(message: types.Message):
    text = [
        '/add_channel - добавить свой канал для публикации постов/редактирования',
        '/my_channels - список ваших каналов',
        '/update_be_versions - обновить версии BE для KB App',
        '/sticker_id - бот вернет айди всех отправленных стикеров',
        '/id - бот вернет ваш id в Telegram',
    ]
    await message.answer('\n'.join(text))\



@rate_limit()
@dp.message_handler(CommandHelp(), IsPrivate())
async def bot_help(message: types.Message):
    text = [
        '/add_channel - добавить свой канал для публикации постов/редактирования',
        '/my_channels - список ваших каналов',
        '/sticker_id - бот вернет айди всех отправленных стикеров',
        '/id - бот вернет ваш id в Telegram',
    ]
    await message.answer('\n'.join(text))
