import random

from aiogram import types

from cat.utils.strings_utils import shuffle
from loader import dp, bot

letters = 26
upper_letters = 65
lower_letters = 97
acceptable_chars = ["!", "?", "#", "_"]


@dp.message_handler(commands="passgen")
async def cowsay_say(message: types.Message):
    args = message.get_args().split(" ")

    size = 8

    if len(args) == 1:
        try:
            size = int(args[0])
        except:
            await bot.send_message(message.chat.id, f"error parsing {args[0]} D:")

    step = int(size / 4)
    overstep = size % 4

    password = ""

    for i in range(step + overstep):
        password += random_upper_char()

    for i in range(step):
        password += random_upper_char()

    for i in range(step):
        password += random.randint(0, 9)

    for i in range(step):
        password += random.choice(acceptable_chars)

    await bot.send_message(message.chat.id, "```" + shuffle(password) + "```", parse_mode="Markdown")


def random_upper_char() -> chr:
    return chr(random.randint(upper_letters, upper_letters + letters - 1))


def random_lower_char() -> chr:
    return chr(random.randint(lower_letters, lower_letters + letters - 1))
