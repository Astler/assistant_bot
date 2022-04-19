from aiogram import types
from telethon import TelegramClient, events
from telethon.tl.types import InputChannel

from data.config import API_HASH, API_ID
from loader import dp


@dp.message_handler(commands="start_wr")
async def bot_help(message: types.Message):
    async with TelegramClient("Ashe - Assistant",
                              API_ID,
                              API_HASH) as client:
        await client.start()

        input_channels_names = ["‼️СИРЕНА. ДНЕПР‼️", "Astler: Dev", "English Pin 📌"]
        output_channel_names = ["Сяся осуждает"]

        input_channels_entities = []
        output_channel_entities = []

        async for d in client.iter_dialogs():
            if d.name in input_channels_names:  # or d.entity.id in config["input_channel_ids"]:
                input_channels_entities.append(InputChannel(d.entity.id, d.entity.access_hash))
            if d.name in output_channel_names:
                output_channel_entities.append(InputChannel(d.entity.id, d.entity.access_hash))

        if not output_channel_entities:
            print(f"Could not find any output channels in the user's dialogs")
            return 0

        if not input_channels_entities:
            print(f"Could not find any input channels in the user's dialogs")
            return 0

        print(
            f"Listening on {len(input_channels_entities)} channels. Forwarding messages to {len(output_channel_entities)} channels.")

        await message.answer("Запущен режим отслеживания сообщений!")

        @client.on(events.NewMessage(chats=input_channels_entities))
        async def handler(event):
            print("EVENT!")
            for output_channel in output_channel_entities:
                await client.forward_messages(output_channel, event.message)

        await client.run_until_disconnected()
