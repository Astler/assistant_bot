import cowsay
from aiogram import types
from aiogram.dispatcher.filters import CommandHelp
from aiogram.types import ParseMode

from filters import IsPrivate, BotAdminsFilter
from loader import dp
from utils.misc import rate_limit
from loader import dp, bot


@dp.message_handler(commands="cowsay")
async def cowsay_say(message: types.Message):
    text = message.get_args()

    if len(text) != 0:
        result = cowsay.get_output_string('cow', text)
        print(result)
        await bot.send_message(message.chat.id, "```" + result + "```", parse_mode="Markdown")
