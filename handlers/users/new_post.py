from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from filters import IsPrivate
from keyboards.base_callback_data import post_creation_callback
from keyboards.sticker_menu import sticker_keyboard, generate_post_keyboard
from loader import dp, bot
from utils.misc import rate_limit
from utils.user_data.data import delete_simple_commands


class PostState(StatesGroup):
    postCreation = State()
    updateContent = State()


@rate_limit()
@dp.message_handler(IsPrivate(), commands=["new_post"])
async def new_post_start(message: types.Message, state: FSMContext):
    if delete_simple_commands(message.from_user.id):
        await message.delete()

    msg = await bot.send_message(chat_id=message.chat.id, text="Что хотите опубликовать?",
                                 reply_markup=generate_post_keyboard())

    async with state.proxy() as data:
        data['request_id'] = msg.message_id

    await PostState.postCreation.set()


@dp.message_handler(state=PostState.postCreation, content_types=types.ContentTypes.TEXT)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        msg_to_delete = data['request_id']
        await message.bot.delete_message(message.chat.id, msg_to_delete)

    msg = await bot.send_message(chat_id=message.chat.id, text=message.text,
                                 reply_markup=generate_post_keyboard("text"))

    async with state.proxy() as data:
        data['request_id'] = msg.message_id
        data['post_type'] = "text"


@dp.message_handler(state=PostState.postCreation, content_types=types.ContentTypes.STICKER)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        msg_to_delete = data['request_id']
        await message.bot.delete_message(message.chat.id, msg_to_delete)

    msg = await bot.send_sticker(chat_id=message.chat.id, sticker=message.sticker.file_id,
                                 reply_markup=generate_post_keyboard("sticker"))

    async with state.proxy() as data:
        data['request_id'] = msg.message_id


@dp.callback_query_handler(post_creation_callback.filter(action="stop"), state=PostState.postCreation)
async def stop_sticker_id(query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(query.message.chat.id, "Пост отменён!")
    await query.message.delete()
    await state.finish()


@dp.callback_query_handler(post_creation_callback.filter(action="edit_text"), state=PostState.postCreation)
async def edit_post_text(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        post_type = data['post_type']

    msg = await bot.send_message(query.message.chat.id, "Введите отредактированный текст!",
                                 reply_markup=generate_post_keyboard("cancel_edit"))
    await query.message.delete()

    async with state.proxy() as data:
        data['request_id'] = msg.message_id

    await PostState.updateContent.set()


@dp.message_handler(state=PostState.updateContent, content_types=types.ContentTypes.TEXT)
async def edit_post_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        post_type = data['post_type']
        msg_to_delete = data['request_id']
        await message.bot.delete_message(message.chat.id, msg_to_delete)

    msg = await bot.send_message(chat_id=message.chat.id, text=message.text,
                                 reply_markup=generate_post_keyboard(post_type))

    async with state.proxy() as data:
        data['request_id'] = msg.message_id

    await message.delete()
    await PostState.postCreation.set()


@dp.callback_query_handler(post_creation_callback.filter(action="publish"), state=PostState.postCreation)
async def edit_post_text(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        post_type = data['post_type']

    await bot.send_message(query.message.chat.id, "DONE!")
    await query.message.delete()
    await state.finish()
