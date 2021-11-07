import ftplib

import requests
from aiogram import types
from bs4 import BeautifulSoup

from data.config import FTP_URL, FTP_USER, FTP_PASS
from filters import IsPrivate, BotAdminsFilter
from loader import dp, bot

import simplejson as json

from utils.misc import rate_limit


class VersionsItem:
    release = ""
    snapshot = ""


@rate_limit()
@dp.message_handler(IsPrivate(), BotAdminsFilter(), commands="update_be_versions")
async def bot_start(message: types.Message):
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

    data = json.JSONEncoder(default=encode_complex, sort_keys=True, indent=4 * ' ', ensure_ascii=False).encode(item)

    await msg.edit_text(f"Данные для загрузки:\n\n{data}")

    f = open("be_versions.json", "w", encoding='utf-8')
    f.write(data)
    f.close()

    file = open('be_versions.json', 'rb')

    with ftplib.FTP(FTP_URL, FTP_USER, FTP_PASS) as ftp, file:
        ftp.storbinary(f'STOR /www/astler.net/apps_data/{file.name}', file)

    await msg.edit_text(f"Данные обновлены!\n\n{data}")
