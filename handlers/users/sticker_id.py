from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from filters import IsPrivate
from keyboards.base_callback_data import sticker_callback
from keyboards.sticker_menu import sticker_keyboard
from loader import dp
from utils.misc import rate_limit
from utils.user_data.data import delete_simple_commands


class StickerState(StatesGroup):
    stickerWait = State()


@rate_limit()
@dp.message_handler(IsPrivate(), commands=["sticker_id"])
async def get_sticker_id(message: types.Message, state: FSMContext):
    if delete_simple_commands(message.from_user.id):
        await message.delete()

    msg = await message.bot.send_message(message.chat.id, "Жду стикер!", reply_markup=sticker_keyboard)

    async with state.proxy() as data:
        data['request_id'] = msg.message_id

    await StickerState.stickerWait.set()


@dp.message_handler(state=StickerState.stickerWait, content_types=types.ContentTypes.STICKER)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        msg_to_delete = data['request_id']
        await message.bot.delete_message(message.chat.id, msg_to_delete)

    await message.reply(message.sticker.file_id)

    msg = await message.bot.send_message(message.chat.id, "Жду стикер!", reply_markup=sticker_keyboard)

    async with state.proxy() as data:
        data['request_id'] = msg.message_id


@dp.message_handler(state=StickerState.stickerWait, content_types=types.ContentTypes.ANY)
async def process_name(message: types.Message, state: FSMContext):
    await message.reply("Это не стикер!")

    msg = await message.bot.send_message(message.chat.id, "Жду стикер!", reply_markup=sticker_keyboard)

    async with state.proxy() as data:
        data['request_id'] = msg.message_id


@dp.callback_query_handler(sticker_callback.filter(action="stop"), state=StickerState.stickerWait)
async def stop_sticker_id(query: types.CallbackQuery, state: FSMContext):
    await query.bot.send_message(query.message.chat.id, "Со стикерами закончили!")
    await query.message.delete()
    await state.finish()
