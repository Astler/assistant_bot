import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from filters import IsPrivate
from keyboards.base_callback_data import cancel_action_callback
from keyboards.sticker_menu import sticker_keyboard
from loader import dp
from utils.misc import rate_limit
from utils.user_data.data import delete_simple_commands


class StickerState(StatesGroup):
    stickerWait = State()


@rate_limit()
@dp.message_handler(IsPrivate(), commands=["sticker_id"])
async def get_sticker_id_start(message: types.Message, state: FSMContext):
    if delete_simple_commands(message.from_user.id):
        await message.delete()

    msg = await message.bot.send_message(message.chat.id, "Жду стикер!", reply_markup=sticker_keyboard)

    async with state.proxy() as data:
        data['request_id'] = msg.message_id

    await StickerState.stickerWait.set()


@dp.message_handler(state=StickerState.stickerWait, content_types=types.ContentTypes.STICKER)
async def get_sticker_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        msg_to_delete = data['request_id']
        await message.bot.delete_message(message.chat.id, msg_to_delete)

    await message.reply(message.sticker.file_id)

    msg = await message.bot.send_message(message.chat.id, "Жду стикер!", reply_markup=sticker_keyboard)

    async with state.proxy() as data:
        data['request_id'] = msg.message_id


@dp.message_handler(state=StickerState.stickerWait, content_types=types.ContentTypes.ANY)
async def no_sticker_error(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        msg_to_delete = data['request_id']
        await message.bot.delete_message(message.chat.id, msg_to_delete)

    reply_msg = await message.reply("Это не стикер!")

    await asyncio.sleep(5)
    await message.delete()
    await reply_msg.delete()

    msg = await message.bot.send_message(message.chat.id, "Жду стикер!", reply_markup=sticker_keyboard)

    async with state.proxy() as data:
        data['request_id'] = msg.message_id


@dp.callback_query_handler(cancel_action_callback.filter(action="cancel"), state=StickerState.stickerWait)
async def stop_sticker_id(query: types.CallbackQuery, state: FSMContext):
    msg = await query.bot.send_message(query.message.chat.id, "Со стикерами закончили!")
    await query.message.delete()
    await state.finish()

    await asyncio.sleep(5)
    await msg.delete()
