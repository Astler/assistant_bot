from aiogram import types
from aiogram.dispatcher.filters import AdminFilter

from filters import IsGroup
from loader import dp, bot
from utils import localization


@dp.message_handler(IsGroup(), AdminFilter(), commands=["ban"])
async def ban(message: types.Message):
    print("text = ", message)

    if not message.reply_to_message:
        await message.reply(localization.get_string("error_no_reply"))
        return

    user = await message.bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    if user.is_chat_admin():
        await message.reply(localization.get_string("error_ban_admin"))
        return

    await message.delete()

    await message.bot.kick_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)

    await message.reply_to_message.reply(localization.get_string("resolved_ban"))


@dp.message_handler(IsGroup(), AdminFilter(), commands=["unban"], commands_prefix="!/")
async def unban(message: types.Message):
    if not message.reply_to_message:
        await message.reply(localization.get_string("error_no_reply"))
        return

    user = await message.bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    if user.is_chat_admin():
        await message.reply(localization.get_string("error_ban_admin"))
        return

    await message.bot.delete_message(message.chat.id, message.message_id)  # remove admin message
    await message.bot.unban_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)

    await message.reply_to_message.reply(localization.get_string("resolved_unban"))
