import asyncio
import logging

import pyrogram
from pyrogram import Client, errors

from aiogram.utils import exceptions as tg_exceptions
from pyrogram.types import Message

from cat.utils.telegram_utils import send_telegram_msg_to_me
from data.config import API_ID, API_HASH, INSTANCE_UNIQUE_NAME, OPENAI_API_KEY
from data.listener_data import get_listener_data
from loader import bot

import openai

openai.api_key = OPENAI_API_KEY

output_channel_id = -1001868505373

should_stop_pyro = False
pyro_task = None
user_app: Client = Client(INSTANCE_UNIQUE_NAME + " Listener", API_ID, API_HASH)


def classify_message(text):
    prompt = f"""I am an AI language model. My task is to classify the following Telegram message into the applicable categories: 'Advertisement', 'Android', 'Unity', 'Development'. A message can belong to multiple categories.

Text: {text}

Please note that:
- 'Advertisement' refers to messages promoting products or services.
- 'Android' refers to messages related to the Android platform or Android apps.
- 'Unity' refers to messages related to the Unity game engine or Unity projects.
- 'Development' refers to messages related to software development, programming, or coding.
- 'Memes' refers to messages containing humorous images, videos, or text.

Categories: """

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )

    categories = response.choices[0].text.strip().split(', ')
    return categories


async def try_to_sign_in(phone_number) -> bool:
    global user_app

    send_telegram_msg_to_me("Visit console to continue! Then try again /listen")

    if user_app.is_connected:
        await user_app.disconnect()

    user_app = Client(INSTANCE_UNIQUE_NAME + " Listener", API_ID, API_HASH, phone_number=phone_number)

    await user_app.start()

    return await try_to_start_listener(user_app)


async def on_channel_post(client, message: Message):
    global should_stop_pyro
    print(f"m {message.chat}")
    listener_data = get_listener_data()

    if message.chat.id not in listener_data.chats_to_listen:
        return

    tags = classify_message(message.text)

    try:
        await bot.send_message(chat_id=output_channel_id, text=f"tags {tags}")
        await bot.forward_message(chat_id=output_channel_id, message_id=message.id, from_chat_id=message.chat.id)
    except Exception as e:
        print(e)
        await user_app.send_message(chat_id=output_channel_id, text=f"tags {tags}")
        await user_app.forward_messages(chat_id=output_channel_id, message_ids=message.id, from_chat_id=message.chat.id)
    print(f"[{message.chat.title}] {message.text}")


async def run_pyrogram():
    global should_stop_pyro
    try:
        await user_app.start()
    except tg_exceptions.NetworkError:
        logging.exception("Failed to connect to Telegram servers")
        return
    while not should_stop_pyro:
        await asyncio.sleep(1)
    await user_app.stop()


async def try_to_start_listener(client: Client = None) -> bool:
    global user_app, pyro_task

    if client is None:
        if user_app.is_connected and not user_app.is_initialized:
            await user_app.disconnect()
        user_app = Client(INSTANCE_UNIQUE_NAME + " Listener", API_ID, API_HASH)
        await user_app.connect()
    else:
        user_app = client

    try:
        await user_app.get_me()
    except (
            errors.ActiveUserRequired,
            errors.AuthKeyInvalid,
            errors.AuthKeyPermEmpty,
            errors.AuthKeyUnregistered,
            errors.AuthKeyDuplicated,
            errors.SessionExpired,
            errors.SessionPasswordNeeded,
            errors.SessionRevoked,
            errors.UserDeactivated,
            errors.UserDeactivatedBan,
    ):
        print("Session invalid / Login failed")
        return False
    else:
        if not user_app.is_initialized:
            await user_app.disconnect()
            await user_app.start()

        print('Login successfully')
        pyro_task = asyncio.ensure_future(run_pyrogram())
        user_app.add_handler(pyrogram.handlers.MessageHandler(on_channel_post, pyrogram.filters.channel))
        return True
