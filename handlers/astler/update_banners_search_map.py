import asyncio
import ftplib

import firebase_admin
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from firebase_admin import credentials, firestore

from data.config import FTP_URL, FTP_USER, FTP_PASS, APPS_DATA_ROOT_URL, PROJECT_ID, BANNERS_MAP_FILE
from filters import IsPrivate, BotAdminsFilter
from keyboards.base_callback_data import simple_callback
from keyboards.publish_keyboard import publish_keyboard, check_keyboard
from loader import dp, bot

import simplejson as json

from utils.admin_data.data import get_cer_data
from utils.misc import rate_limit


class BannerServerItem:
    name = ""
    id = ""
    date = ""


class DataBannersState(StatesGroup):
    actionUserWait = State()


@rate_limit()
@dp.message_handler(IsPrivate(), BotAdminsFilter(), commands="update_banners_search_map")
async def get_data_from_firebase(message: types.Message, state: FSMContext):
    msg = await bot.send_message(message.chat.id, "Подключаюсь к Firebase...")
    cred = credentials.Certificate(get_cer_data())

    firebase_admin.initialize_app(cred, {
        'projectId': PROJECT_ID,
    })

    db = firestore.client()

    await msg.edit_text("Готово! Получаю баннеры...")

    users_ref = db.collection(u'shared_banners')
    docs = users_ref.stream()

    items = []

    for doc in docs:
        resultdict = doc.to_dict()
        innerItem = BannerServerItem()
        innerItem.name = resultdict["mbannerName"]
        innerItem.id = resultdict["mid"]
        innerItem.date = resultdict["mdate"]
        items.append(innerItem)

    def encode_complex(obj):
        if isinstance(obj, BannerServerItem):
            return {
                "id": obj.id, "name": obj.name, "date": obj.date
            }
        raise TypeError(repr(obj) + " is not JSON serializable")

    json_data = json.JSONEncoder(default=encode_complex, sort_keys=True, indent=4 * ' ', ensure_ascii=False) \
        .encode(items)

    f = open(BANNERS_MAP_FILE, "w", encoding='utf-8')
    f.write(json_data)
    f.close()

    await msg.edit_text(f"Для загрузки найдено {len(items)} баннеров!", reply_markup=publish_keyboard())

    async with state.proxy() as data:
        data['request_id'] = msg.message_id

    f = open(BANNERS_MAP_FILE, "w", encoding='utf-8')
    f.write(json_data)
    f.close()

    await DataBannersState.actionUserWait.set()


@dp.callback_query_handler(simple_callback.filter(action="publish"), state=DataBannersState.actionUserWait)
async def publish_new_data(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as state_data:
        msg = state_data['request_id']

    file = open(BANNERS_MAP_FILE, 'rb')

    with ftplib.FTP(FTP_URL, FTP_USER, FTP_PASS) as ftp, file:
        ftp.storbinary(f'STOR /astler.net/apps_data/{file.name}', file)

    await bot.edit_message_text(f"Данные обновлены!\n\n", query.message.chat.id, msg,
                                reply_markup=check_keyboard(APPS_DATA_ROOT_URL + BANNERS_MAP_FILE))
    await state.finish()


@dp.callback_query_handler(simple_callback.filter(action="cancel"), state=DataBannersState.actionUserWait)
async def cancel_operation(query: types.CallbackQuery, state: FSMContext):
    msg = await query.bot.send_message(query.message.chat.id, "Операция отменена!")
    await query.message.delete()
    await state.finish()

    await asyncio.sleep(5)
    await msg.delete()
