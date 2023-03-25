from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.listener.listener import try_to_start_listener, try_to_sign_in
from filters import BotAdminsFilter
from loader import dp, bot


# can send messages from channels where bot is in
# @dp.channel_post_handler(lambda message: message.chat.id in input_channel_ids)
# async def forward_message(message: types.Message):
#     await bot.forward_message(output_channel_id, message.chat.id, message.message_id)


class SignIn(StatesGroup):
    wait_phone_number = State()


@dp.message_handler(BotAdminsFilter(), commands=['listen'])
async def cmd_signin(message: types.Message):
    if await try_to_start_listener():
        await message.answer("Already authorized!")
        return

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

    await message.reply(f"Got it! {phone_number}", reply_markup=None)

    if await try_to_sign_in(phone_number):
        await message.answer("You have been authorized!")
    else:
        await message.answer("Something went wrong")

    await state.finish()
