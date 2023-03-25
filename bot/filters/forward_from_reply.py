from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

class ForwardFromReply(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        reply_to = message.reply_to_message

        if reply_to is None:
            await message.answer("This command requires to be called on reply!")
            return False

        origin_chat = reply_to.forward_from_chat

        if origin_chat is None:
            await message.answer("Reply message should be forwarded from chat!")
            return False

        return True
