import cowsay
from aiogram import types
from aiogram.dispatcher.filters import CommandHelp
from aiogram.types import ParseMode

from filters import IsPrivate, BotAdminsFilter
from loader import dp
from utils.misc import rate_limit
from loader import dp, bot


@dp.message_handler(commands="cowsay", prefixes="!/")
async def cowsay_say(message: types.Message):
    text = message.get_args()

    if len(text) != 0:
        await bot.send_message(message.chat.id, cowsay.get_output_string('cow', text))
