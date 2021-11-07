from aiogram import types

from filters import IsPrivate
from keyboards.my_channels_keyboard import generate_user_channels_keyboard
from loader import dp, bot
from utils.user_data.data import get_user_channels, delete_simple_commands


@dp.message_handler(IsPrivate(), commands=["my_channels"])
async def options(message: types.Message):
    if delete_simple_commands(message.from_user.id):
        await message.delete()

    channels_ids = get_user_channels(message.from_user.id)

    channels = {}

    for channel_id in channels_ids:
        chat = await bot.get_chat(channel_id)
        chat_url = await chat.get_url()
        channels[chat_url] = chat.title

    if len(channels) != 0:
        await bot.send_message(chat_id=message.chat.id, text="Ваши каналы",
                               reply_markup=generate_user_channels_keyboard(channels))
    else:
        await bot.send_message(chat_id=message.chat.id, text="Похоже, что вы ещё не добавили ни одного канала")
