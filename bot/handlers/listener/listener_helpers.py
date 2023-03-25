from aiogram import types


async def check_is_reply_message(message: types.Message) -> bool:
    reply_to = message.reply_to_message

    if reply_to is None:
        await message.answer("You should reply message from channel in chat!")
        return False

    origin_chat = reply_to.forward_from_chat

    if origin_chat is None:
        await message.answer("You should reply to forwarded message from channel!")
        return False

    reply_chat_id = origin_chat.id
    current_chat_id = message.chat.id

    if reply_chat_id == current_chat_id:
        await message.answer("Reply to same chat!")
        return False
