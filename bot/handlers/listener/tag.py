from aiogram import types

from bot.filters.forward_from_reply import ForwardFromReply
from bot.listener.listener_data import get_listener_data, save_listener_data
from filters import BotSuperAdminsFilter
from loader import dp


@dp.message_handler(BotSuperAdminsFilter(), ForwardFromReply(), commands=['tag'])
async def cmd_tag_for_chat(message: types.Message):
    listener_data = get_listener_data()

    reply_chat_id = message.reply_to_message.forward_from_chat.id

    chats = listener_data.chats_to_listen
    chat = chats[reply_chat_id]
    chat.hashtag = message.text.split()[1]
    chats[reply_chat_id] = chat
    listener_data.chats_to_listen = chats

    save_listener_data(listener_data)

    await message.answer(f"Updated hashtags!! {chat.hashtag}")
