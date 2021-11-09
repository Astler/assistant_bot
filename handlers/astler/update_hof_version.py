import requests
import simplejson as json
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ParseMode

from filters import IsPrivate, BotAdminsFilter
from loader import dp, bot
from utils.misc import rate_limit


class HOFItem:
    name = ""
    description = ""
    sort = 0


class DataState(StatesGroup):
    actionWait = State()


@rate_limit()
@dp.message_handler(IsPrivate(), BotAdminsFilter(), commands="update_hof_versions")
async def bot_start(message: types.Message, state: FSMContext):
    msg = await bot.send_message(message.chat.id, "Начинаю загрузку данных HOF...")

    URL = "https://astler.net/apps_data/hof.json"
    page = requests.get(URL).text

    hof_json_array = json.loads(page)

    hof_list = []
    output_msg = []

    for item in hof_json_array:
        hof_item = HOFItem()
        hof_item.name = item['mName']
        hof_item.description = item['mDescription']
        output_msg.append(f"*{hof_item.name}*\n{hof_item.description}")
        hof_list.append(hof_item)

    data_from_server = "\n\n".join(output_msg)

    print(data_from_server)

    await msg.edit_text(f"Спасибо всем, кто помогал и продолжает помогать!\n\n{data_from_server}", parse_mode=ParseMode.MARKDOWN)

#     async with state.proxy() as data:
#         data['data_to_publish'] = json_data
#         data['request_id'] = msg.message_id
#
#     await DataState.actionWait.set()
#
#
# @dp.callback_query_handler(simple_callback.filter(action="publish"), state=DataState.actionWait)
# async def publish_new_data(query: types.CallbackQuery, state: FSMContext):
#     async with state.proxy() as state_data:
#         data_to_publish = state_data['data_to_publish']
#         msg = state_data['request_id']
#
#     f = open(BE_VERSIONS_FILE, "w", encoding='utf-8')
#     f.write(data_to_publish)
#     f.close()
#
#     file = open(BE_VERSIONS_FILE, 'rb')
#
#     with ftplib.FTP(FTP_URL, FTP_USER, FTP_PASS) as ftp, file:
#         ftp.storbinary(f'STOR /www/astler.net/apps_data/{file.name}', file)
#
#     await bot.edit_message_text(f"Данные обновлены!\n\n{data_to_publish}", query.message.chat.id, msg,
#                                 reply_markup=check_keyboard(APPS_DATA_ROOT_URL + BE_VERSIONS_FILE))
#     await state.finish()
#
#
# @dp.callback_query_handler(simple_callback.filter(action="cancel"), state=DataState.actionWait)
# async def cancel_operation(query: types.CallbackQuery, state: FSMContext):
#     msg = await query.bot.send_message(query.message.chat.id, "Операция отменена!")
#     await query.message.delete()
#     await state.finish()
#
#     await asyncio.sleep(5)
#     await msg.delete()
