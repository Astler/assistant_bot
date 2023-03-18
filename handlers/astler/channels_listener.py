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

input_channel_ids = [-1001234567890, -1001234567891]  # List of input channel IDs


@dp.channel_post_handler(lambda message: message.chat.id in input_channel_ids)
async def forward_message(message: types.Message):
    await bot.forward_message(output_channel_id, message.chat.id, message.message_id)


class SignIn(StatesGroup):
    wait_phone_number = State()
    phone_number = State()
    verification_code = State()


@dp.message_handler(commands=['listen'])
async def cmd_signin(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button = KeyboardButton("Share your phone number", request_contact=True)
    keyboard.add(button)

    await message.reply("Please share your phone number:", reply_markup=keyboard)

    await SignIn.wait_phone_number.set()


@dp.message_handler(state=SignIn.wait_phone_number, content_types=[types.ContentType.CONTACT])
async def process_phone_number(message: types.Message, state: FSMContext):
    contact = message.contact
    phone_number = contact.phone_number

    async with state.proxy() as data:
        data['phone_number'] = phone_number

    await SignIn.phone_number.set()


@dp.message_handler(state=SignIn.phone_number)
async def process_phone_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone_number'] = message.text

    client = TelegramClient(INSTANCE_UNIQUE_NAME, API_ID, API_HASH)
    await client.connect()

    if not await client.is_user_authorized():
        print(f"yes {data['phone_number']}")
        await client.send_code_request(data['phone_number'])
        await bot.send_message(message.chat.id, text="Please enter the code you received:")
    else:
        print("no")

    print("finish number step")
    await SignIn.verification_code.set()


@dp.message_handler(state=SignIn.verification_code)
async def process_verification_code(message: types.Message, state: FSMContext):
    print("start verification_code step")
    async with state.proxy() as data:
        phone_number = data['phone_number']
        verification_code = message.text

    print(verification_code)

    try:
        client = TelegramClient(INSTANCE_UNIQUE_NAME, API_ID, API_HASH)
        await client.connect()
        await client.start(phone=phone_number, code_callback=lambda: verification_code, password=lambda: "1999212")

        if await client.is_user_authorized():
            await message.answer("You have been authorized!")

        print("some")

        @client.on(events.NewMessage(chats=input_channels_names))
        async def forward_messages(event):
            await bot.forward_message(output_channel_id, event.chat_id, event.message.id)

        await client.run_until_disconnected()
    except Exception as e:
        print(e)
        await message.answer(f"Authorization failed: {e}")

    # reset the state
    await state.finish()
