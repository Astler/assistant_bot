import re

from aiogram import types
from aiogram.dispatcher.filters import AdminFilter

from filters import IsGroup
from loader import dp

from utils.group_data.data import get_group_info, get_blocked_links, save_group_dict


@dp.message_handler(IsGroup(), AdminFilter(), commands=["add_black_link"])
async def black_link_edit(message: types.Message):
    group_dict = get_group_info(message.chat.id)

    command_parse = re.compile(r"(!add_black_link|/add_black_link|/add_black_link@cat_assistant_bot) ?([a-zA-Zа-яА-Я. ]+)?")
    parsed = command_parse.match(message.text)
    new_value = parsed.group(2)

    if not new_value:
        await message.bot.send_message(message.chat.id, f"group_dict = {group_dict}")
    else:
        print(new_value)
        current = get_blocked_links(message.chat.id)

        if current is None:
            current = []

        current.append(new_value.lower())
        group_dict["blocked_links"] = current

        save_group_dict(message.chat.id, group_dict)





