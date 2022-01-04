from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from filters import IsGroup
from filters.is_only_dots_in_msg import IsDotsMessage
from loader import dp


@dp.message_handler(IsDotsMessage())
async def bot_start(message: types.Message):
    await message.reply('╭∩╮（︶_︶）╭∩╮')
