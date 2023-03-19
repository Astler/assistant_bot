import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from telethon import TelegramClient, events

from data.config import API_HASH, API_ID, INSTANCE_UNIQUE_NAME
from filters import BotAdminsFilter
from loader import dp, bot

input_channels_names = ["@lazy_astler", "@the_english_pin"]
output_channel_id = -1001216924947

input_channel_ids = [-1001234567890, -1001234567891]


@dp.channel_post_handler(lambda message: message.chat.id in input_channel_ids)
async def forward_message(message: types.Message):
    await bot.forward_message(output_channel_id, message.chat.id, message.message_id)


class SignIn(StatesGroup):
    wait_phone_number = State()


@dp.message_handler(BotAdminsFilter, commands=['listen'])
async def cmd_signin(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button = KeyboardButton("Share your phone number", request_contact=True)
    keyboard.add(button)

    await message.reply("Please share your phone number to continue:", reply_markup=keyboard)

    await SignIn.wait_phone_number.set()


@dp.message_handler(state=SignIn.wait_phone_number, content_types=[types.ContentType.CONTACT])
async def process_phone_number(message: types.Message, state: FSMContext):
    contact = message.contact
    phone_number = contact.phone_number

    async with state.proxy() as data:
        data['phone_number'] = phone_number

    await message.reply("Got it!", reply_markup=None)

    client = TelegramClient(INSTANCE_UNIQUE_NAME, API_ID, API_HASH)
    await client.connect()
    await client.start(phone=phone_number)

    if not await client.is_user_authorized():
        print(f"yes {data['phone_number']}")
        await client.send_code_request(data['phone_number'])
        await bot.send_message(message.chat.id, text="Visit console to continue! Then try again /listen")
        await state.finish()
    else:
        print("User already authorized.")
        if await client.is_user_authorized():
            await message.answer("You have been authorized!")
        else:
            await message.answer("Something went wrong")

        @client.on(events.NewMessage(chats=input_channels_names))
        async def forward_messages(event):
            await bot.forward_message(output_channel_id, event.chat_id, event.message.id)

        asyncio.create_task(client.run_until_disconnected())

        await state.finish()
