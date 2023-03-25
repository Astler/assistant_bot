from aiogram import types

from bot.filters.forward_from_reply import ForwardFromReply
from data.listener_data import get_listener_data, ChatToListenData, save_listener_data
from filters import BotSuperAdminsFilter
from loader import dp


@dp.message_handler(BotSuperAdminsFilter(), ForwardFromReply(), commands=['add'])
async def cmd_add_to_listener(message: types.Message):
    reply_chat_id = message.reply_to_message.forward_from_chat.id

    if reply_chat_id == message.chat.id:
        await message.answer("You can't add yourself to listener!")
        return

    listener_data = get_listener_data()

    if listener_data.chats_to_listen.__contains__(reply_chat_id):
        await message.answer("Already added to listener!")
        return

    chats = listener_data.chats_to_listen
    chats[reply_chat_id] = ChatToListenData(reply_chat_id)
    listener_data.chats_to_listen = chats

    save_listener_data(listener_data)

    await message.answer("Added to listener!")
