import asyncio

from telethon import TelegramClient, events
from telethon.tl.types import InputChannel

from cat.utils.telegram_utils import send_telegram_msg_to_me
from data.config import INSTANCE_UNIQUE_NAME, API_ID, API_HASH
from loader import bot

output_channel_id = -1001216924947

input_channel_ids = [-1001234567890, -1001234567891]


async def try_to_sign_in(phone_number) -> bool:
    client = TelegramClient(INSTANCE_UNIQUE_NAME, API_ID, API_HASH)

    send_telegram_msg_to_me("Visit console to continue! Then try again /listen")
    await client.connect()
    await client.start(phone=phone_number)

    if await client.is_user_authorized():
        await setup_listener(client)
        return True
    else:
        send_telegram_msg_to_me("Something went wrong")
        return False

async def try_to_start_listener() -> bool:
    client = TelegramClient(INSTANCE_UNIQUE_NAME, API_ID, API_HASH)
    await client.connect()

    if await client.is_user_authorized():
        await client.start()
        send_telegram_msg_to_me("Listener started!")
        await setup_listener(client)
        return True

    return False


async def setup_listener(client):
    input_channels = await get_input_channels(client)

    @client.on(events.NewMessage(chats=input_channels))
    async def forward_messages(event):
        try:
            await bot.forward_message(output_channel_id, event.chat_id, event.message.id)
        except:
            await client.forward_messages(output_channel_id, event.message)

    asyncio.create_task(client.run_until_disconnected())


async def get_input_channels(client):
    input_channels_names = ["‼️СИРЕНА. ДНЕПР‼️", "Astler: Dev", "English Pin 📌"]

    input_channels_entities = []

    async for d in client.iter_dialogs():
        if d.name in input_channels_names:  # or d.entity.id in config["input_channel_ids"]:
            input_channels_entities.append(InputChannel(d.entity.id, d.entity.access_hash))


    if not input_channels_entities:
        print(f"Could not find any input channels in the user's dialogs")
        return []

    return input_channels_entities
