from aiogram import types

from bot.handlers.listener.listener_helpers import check_is_reply_message
from data.listener_data import get_listener_data, ChatToListenData, save_listener_data
from filters import BotAdminsFilter
from loader import dp


@dp.message_handler(BotAdminsFilter(), commands=['add'])
async def cmd_add_to_listener(message: types.Message):
    listener_data = get_listener_data()

    if not check_is_reply_message(message):
        return

    reply_chat_id = message.reply_to_message.forward_from_chat.id

    if listener_data.chats_to_listen.__contains__(reply_chat_id):
        return await message.answer("Already added to listener!")

    chats = listener_data.chats_to_listen

    chats[reply_chat_id] = ChatToListenData(reply_chat_id)

    listener_data.chats_to_listen = chats

    save_listener_data(listener_data)

    await message.answer("Added to listener!")
