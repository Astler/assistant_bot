from aiogram import types

from data.listener_data import get_listener_data, ChatToListenData, save_listener_data
from filters import BotAdminsFilter
from loader import dp


@dp.message_handler(BotAdminsFilter(), commands=['tag'])
async def cmd_tag_for_chat(message: types.Message):
    listener_data = get_listener_data()

    reply_to = message.reply_to_message

    print(message)

    if reply_to is None:
        await message.answer("You should reply message from channel in chat!")
        return

    origin_chat = reply_to.forward_from_chat

    if origin_chat is None:
        return await message.answer("You should reply to forwarded message from channel!")

    reply_chat_id = origin_chat.id
    current_chat_id = message.chat.id

    if reply_chat_id == current_chat_id:
        return await message.answer("You can't add yourself to listener!")

    if not listener_data.chats_to_listen.__contains__(reply_chat_id):
        await message.answer("You cant add hashtag to not listening chat!")
        return

    chats = listener_data.chats_to_listen

    chat = chats[reply_chat_id]

    chat.hashtag = message.text.split()[1]

    print(chat.hashtag)

    chats[reply_chat_id] = chat
    listener_data.chats_to_listen = chats

    save_listener_data(listener_data)

    await message.answer(f"Updated hashtags!! {chat.hashtag}")
