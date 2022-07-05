from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import ForwardedMessageFilter
from aiogram.dispatcher.filters.state import StatesGroup, State

from filters import IsPrivate
from keyboards.base_callback_data import cancel_action_callback
from keyboards.sticker_menu import add_channel_keyboard
from loader import dp, bot
from utils.user_data.data import add_user_channel


class AddChannelState(StatesGroup):
    waitMsgFromNewChannel = State()


@dp.message_handler(IsPrivate(), commands=["add_channel"])
async def options(message: types.Message, state: FSMContext):
    msg = await bot.send_message(chat_id=message.chat.id, text="Чтобы добавить бота в свой список - добавьте бота на "
                                                               "свой канал и предоставьте ему права админа. После "
                                                               "этого перешлите сообщение из этого канала. Если всё "
                                                               "сделано - канал будет добавлен.",
                                 reply_markup=add_channel_keyboard)

    async with state.proxy() as data:
        data['request_id'] = msg.message_id

    await AddChannelState.waitMsgFromNewChannel.set()


@dp.message_handler(ForwardedMessageFilter(is_forwarded=True), state=AddChannelState.waitMsgFromNewChannel)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        msg_to_delete = data['request_id']
        await message.bot.delete_message(message.chat.id, msg_to_delete)

    chat = message.forward_from_chat.id

    member_status = await bot.get_chat_member(chat, bot.id)

    if member_status.is_chat_admin():
        msg = await bot.send_message(chat_id=message.chat.id, text="Отлично! Канал добавлен")
        add_user_channel(message.from_user.id, chat)
        await state.finish()
    else:
        msg = await bot.send_message(chat_id=message.chat.id, text="Что-то пошло не так. Бот точно админ?",
                                     reply_markup=add_channel_keyboard)

    async with state.proxy() as data:
        data['request_id'] = msg.message_id


@dp.message_handler(state=AddChannelState.waitMsgFromNewChannel)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        msg_to_delete = data['request_id']
        await message.bot.delete_message(message.chat.id, msg_to_delete)

    msg = await bot.send_message(chat_id=message.chat.id, text="Перешлите сообщение из целевого канала!",
                                 reply_markup=add_channel_keyboard)

    async with state.proxy() as data:
        data['request_id'] = msg.message_id


@dp.callback_query_handler(cancel_action_callback.filter(action="cancel"), state=AddChannelState.waitMsgFromNewChannel)
async def stop_sticker_id(query: types.CallbackQuery, state: FSMContext):
    await query.bot.send_message(query.message.chat.id, "Окей, отмена!")
    await query.message.delete()
    await state.finish()
