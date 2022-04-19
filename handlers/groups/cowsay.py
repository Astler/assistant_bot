import cowsay
from aiogram import types

from loader import dp, bot


@dp.message_handler(commands="cowsay")
async def cowsay_say(message: types.Message):
    args = message.get_args().split(" cow=")

    if len(args) == 0:
        return

    if len(args) == 1:
        text = str(args[0])
        character = "cow"
    else:
        text = str(args[0])
        character = str(args[1])

    if len(text) != 0:
        result = cowsay.get_output_string(character, text)
        print(result)
        await bot.send_message(message.chat.id, "```" + result + "```", parse_mode="Markdown")


@dp.message_handler(commands="cowsay_help")
async def cowsay_say(message: types.Message):
    await bot.send_message(message.chat.id, cowsay.char_names)
