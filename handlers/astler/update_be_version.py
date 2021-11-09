import asyncio
import ftplib

import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from bs4 import BeautifulSoup

from data.config import FTP_URL, FTP_USER, FTP_PASS, BE_VERSIONS_FILE, APPS_DATA_ROOT_URL
from filters import IsPrivate, BotAdminsFilter
from keyboards.base_callback_data import simple_callback
from keyboards.publish_keyboard import publish_keyboard, check_keyboard
from loader import dp, bot

import simplejson as json

from utils.misc import rate_limit


class VersionsItem:
    release = ""
    snapshot = ""


class DataState(StatesGroup):
    actionWait = State()


@rate_limit()
@dp.message_handler(IsPrivate(), BotAdminsFilter(), commands="update_be_versions")
async def bot_start(message: types.Message, state: FSMContext):
    msg = await bot.send_message(message.chat.id, "Начинаю загрузку данных из вики...")

    URL = "https://minecraft.fandom.com/ru/wiki/Bedrock_Edition"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find(class_="infobox-rows")

    more_results = results.find_all("a")

    output_string = ""

    item = VersionsItem()
    found = []

    for a in more_results:
        if str(a.get('title', '')).__contains__("(Bedrock Edition)"):
            href = str(a.get('href', ''))
            href_array = href.split("/")
            found.append(href_array[len(href_array) - 1])
            print(href)

            output_string += a.text

    if len(found) >= 2:
        item.release = found[0]
        item.snapshot = found[1]
    else:
        if len(found) != 0:
            item.release = found[0]

    def encode_complex(obj):
        if isinstance(obj, VersionsItem):
            return {
                "snapshot": obj.snapshot, "release": obj.release
            }
        raise TypeError(repr(obj) + " is not JSON serializable")

    json_data = json.JSONEncoder(default=encode_complex, sort_keys=True, indent=4 * ' ', ensure_ascii=False).encode(
        item)

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

    f = open(BE_VERSIONS_FILE, "w", encoding='utf-8')
    f.write(data_to_publish)
    f.close()

    file = open(BE_VERSIONS_FILE, 'rb')

    with ftplib.FTP(FTP_URL, FTP_USER, FTP_PASS) as ftp, file:
        ftp.storbinary(f'STOR /www/astler.net/apps_data/{file.name}', file)

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
