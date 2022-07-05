import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from data.config import BE_VERSIONS_FILE, APPS_DATA_ROOT_URL
from filters import IsPrivate, BotAdminsFilter
from keyboards.base_callback_data import simple_callback
from keyboards.publish_keyboard import publish_keyboard, check_keyboard
from loader import dp, bot
from utils.minecraft.be_version_updater import be_version_get, be_version_push
from utils.misc import rate_limit


class DataState(StatesGroup):
    actionWait = State()


@rate_limit()
@dp.message_handler(IsPrivate(), BotAdminsFilter(), commands="update_be_versions")
async def bot_start(message: types.Message, state: FSMContext):
    msg = await bot.send_message(message.chat.id, "Начинаю загрузку данных из вики...")

    json_data = await be_version_get()

    await msg.edit_text(f"Данные для загрузки:\n\n{json_data}", reply_markup=publish_keyboard())

    async with state.proxy() as data:
        data['data_to_publish'] = json_data
        data['request_id'] = msg.message_id

    await DataState.actionWait.set()


@dp.callback_query_handler(simple_callback.filter(action="publish"), state=DataState.actionWait)
async def publish_new_data(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as state_data:
        data_to_publish = state_data['data_to_publish']
        msg = state_data['request_id']

    await be_version_push(data_to_publish)

    await bot.edit_message_text(f"Данные обновлены!\n\n{data_to_publish}", query.message.chat.id, msg,
                                reply_markup=check_keyboard(APPS_DATA_ROOT_URL + BE_VERSIONS_FILE))
    await state.finish()


@dp.callback_query_handler(simple_callback.filter(action="cancel"), state=DataState.actionWait)
async def cancel_operation(query: types.CallbackQuery, state: FSMContext):
    msg = await query.bot.send_message(query.message.chat.id, "Операция отменена!")
    await query.message.delete()
    await state.finish()

    await asyncio.sleep(5)
    await msg.delete()
