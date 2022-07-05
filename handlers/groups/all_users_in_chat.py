from aiogram import types

from handlers.groups.rep_system_group import create_user_mention
from loader import dp, bot, app


@dp.message_handler(commands=["all_members", "all_abroad"])
async def users_in_this_chat(message: types.Message):
    all_in_chat = []

    async for member in app.get_chat_members(message.chat.id):
        all_in_chat.append(create_user_mention(member))

    await bot.send_message(message.chat.id, "\n".join(all_in_chat), parse_mode="Markdown")
