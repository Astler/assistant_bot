from aiogram import types

from filters.is_only_dots_in_msg import IsDotsMessage
from loader import dp


@dp.message_handler(IsDotsMessage())
async def bot_start(message: types.Message):
    if message.from_user.id != 1072483718:
        await message.reply('╭∩╮（︶_︶）╭∩╮')
