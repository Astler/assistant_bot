import re

from aiogram import types

from filters import IsPrivate
from loader import dp

from utils.user_data.data import get_user_dict, save_user_dict, delete_simple_commands


@dp.message_handler(IsPrivate(), commands=["profile"])
async def options(message: types.Message):
    user_dict = get_user_dict(message.from_user.id)

    command_parse = re.compile(r"(!profile|/profile|/profile@cat_assistant_bot) ?([a-zA-Zа-яА-Я ]+)?")
    parsed = command_parse.match(message.text)
    new_value = parsed.group(2)

    if not new_value:
        if delete_simple_commands(message.from_user.id):
            await message.delete()
        await message.bot.send_message(message.chat.id, f"user_dict = {user_dict}")
    else:
        lower_value = new_value.lower()

        if lower_value == "true" or lower_value == "false":

            if lower_value == "true":
                user_dict["delete_simple_command_requests"] = True
            else:
                user_dict["delete_simple_command_requests"] = False

            save_user_dict(message.from_user.id, user_dict)

            await message.bot.send_message(message.chat.id, f"new_value = {lower_value}")
        else:
            await message.bot.send_message(message.chat.id, f"incorrect value")
