from aiogram import types
from pyrogram import Client

from data.config import BOT_TOKEN, API_ID, API_HASH
from handlers.groups.rep_system_group import create_user_mention
from loader import dp, bot


@dp.message_handler(commands="all_in_chat")
async def my_rep(message: types.Message):
    app = Client(
        BOT_TOKEN,
        api_id=API_ID,
        api_hash=API_HASH
    )
    await app.start()
    members = await app.get_chat_members(message.chat.id)

    all_in_chat = []

    for member in members:
        all_in_chat.append(create_user_mention(member))

    await bot.send_message(message.chat.id, "\n".join(all_in_chat), parse_mode="Markdown")

    await app.stop()
