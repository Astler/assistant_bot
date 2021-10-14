import asyncio
import datetime
import re

from aiogram import types
from aiogram.dispatcher.filters import Command, AdminFilter

from filters import IsGroup
from loader import dp, bot
from utils import localization


@dp.message_handler(IsGroup(), Command("ro", prefixes="!/"), AdminFilter())
async def set_read_only_mode(message: types.Message):
    if not message.reply_to_message:
        await message.reply(localization.get_string("can_be_used_with_reply"))
        return

    member = message.reply_to_message.from_user.id
    member_name = message.reply_to_message.from_user.full_name
    chat_id = message.chat.id
    command_parse = re.compile(r"(!ro|/ro|/ro@cat_assistant_bot) ?([a-zA-Zа-яА-Я ]+)? ?(\d+)?")
    parsed = command_parse.match(message.text)
    comment = parsed.group(2)
    time = parsed.group(3)

    if not time:
        time = 5
    else:
        time = int(time)

    until_date = datetime.datetime.now() + datetime.timedelta(minutes=time)

    read_only_permissions = types.ChatPermissions(
        can_send_messages=False,
        can_send_media_messages=False,
        can_send_polls=False,
        can_send_other_messages=False,
        can_add_web_page_previews=False,
        can_invite_users=True,
        can_change_info=False,
        can_pin_messages=False
    )

    try:
        await bot.restrict_chat_member(chat_id, user_id=member, permissions=read_only_permissions,
                                       until_date=until_date)

        if comment is None:
            reason = "Не указана"
        else:
            reason = comment

        await message.answer(f"Пользователю {member_name} запрещено писать на {time} минут.\n\nПричина: {reason}.")
    except Exception as err:
        await message.answer("Пользователь Админ!" + err.__class__.__name__)

    await message.delete()


@dp.message_handler(IsGroup(), Command("ro", prefixes="!/"))
async def set_read_only_mode_not_admin(message: types.Message):
    answer_message = await message.reply(localization.get_string("this_command_only_for_admins"))
    await message.delete()
    await asyncio.sleep(3)
    await answer_message.delete()


@dp.message_handler(Command("ro", prefixes="!/"))
async def set_read_only_mode_not_admin(message: types.Message):
    answer_message = await message.reply(localization.get_string("ro_in_personal_messages"))
    await message.delete()
    await asyncio.sleep(3)
    await answer_message.delete()
