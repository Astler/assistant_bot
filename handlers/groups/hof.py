import urllib.request

import simplejson as json
from aiogram import types
from aiogram.types import ParseMode

from filters import IsGroup
from loader import dp, bot
from utils.misc import rate_limit


class HOFItem:
    name = ""
    description = ""
    sort = 0


@rate_limit()
@dp.message_handler(IsGroup(), commands="hof")
async def get_hof(message: types.Message):
    msg = await bot.send_message(message.chat.id, "Начинаю загрузку данных HOF...")

    with urllib.request.urlopen("https://astler.net/apps_data/hof.json") as url:
        data = url.read().decode()

        hof_json_array = json.loads(data)

        output_msg = []

        for item in hof_json_array:
            hof_item = HOFItem()
            hof_item.name = item['mName']
            hof_item.description = item['mDescription']
            output_msg.append(f"*{hof_item.name}*\n{hof_item.description}")

        data_from_server = ("\n\n".join(output_msg)).replace("!", "\!").replace("-", "\-")

        await msg.edit_text(f"Спасибо всем, кто принимает участие в развитии приложений!\n\nЕсли помогали и не нашли "
                            f"себя в списке - пишите, обязательно добавлю!\n\n{data_from_server}",
                            parse_mode=ParseMode.MARKDOWN)
