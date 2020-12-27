import asyncio
import datetime
import re

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.utils.exceptions import BadRequest

from filters import IsGroup, AdminFilter
from loader import dp, bot


@dp.message_handler(IsGroup(), Command("ro", prefixes="!/"), AdminFilter())
async def set_ro_mode(message: types.Message):
    member = message.reply_to_message.from_user.id
    member_name = message.reply_to_message.from_user.full_name
    chat_id = message.chat.id
    command_parse = re.compile(r"(!ro|/ro) ?(\d+)? ?([a-zA-Z ]+)?")
    parsed = command_parse.match(message.text)
    time = parsed.group(2)
    comment = parsed.group(3)

    if not time:
        time = 5
    else:
        time = int(time)

    until_date = datetime.datetime.now() + datetime.timedelta(minutes=time)

    ReadOnlyPermissions = types.ChatPermissions(
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
        await bot.restrict_chat_member(chat_id, user_id=member, permissions=ReadOnlyPermissions,
                                       until_date=until_date)
        await message.answer(f"Пользователю {member_name} запрещено писать на {time} минут. Причина: {comment}")
    except Exception as err:
        await message.answer("Пользователь Админ!" + err.__class__.__name__)

    service_message = await message.reply("Это сообщение будет удалено через 5 секунд!")
    await asyncio.sleep(5)
    await message.delete()
    await service_message.delete()
