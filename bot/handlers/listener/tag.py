from aiogram import types

from bot.handlers.listener.listener_helpers import check_is_reply_message
from data.listener_data import get_listener_data, ChatToListenData, save_listener_data
from filters import BotAdminsFilter
from loader import dp


@dp.message_handler(BotAdminsFilter(), commands=['tag'])
async def cmd_tag_for_chat(message: types.Message):
    listener_data = get_listener_data()

    if not check_is_reply_message(message):
        return

    reply_chat_id = message.reply_to_message.forward_from_chat.id

    chats = listener_data.chats_to_listen

    chat = chats[reply_chat_id]

    chat.hashtag = message.text.split()[1]

    print(chat.hashtag)

    chats[reply_chat_id] = chat
    listener_data.chats_to_listen = chats

    save_listener_data(listener_data)

    await message.answer(f"Updated hashtags!! {chat.hashtag}")
