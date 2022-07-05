import ftplib
import logging

import requests
import simplejson as json
from bs4 import BeautifulSoup

from data.config import BE_VERSIONS_FILE, FTP_URL, FTP_USER, FTP_PASS
from loader import dp
from utils.notify_admins import send_msg_to_admin


class VersionsItem:
    release = ""
    snapshot = ""


async def be_version_get():
    logging.info("connecting to wiki")

    url = "https://minecraft.fandom.com/wiki/Bedrock_Edition"
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find(class_="infobox-rows")

    more_results = results.find_all("tr")

    item = VersionsItem()
    found = []

    logging.info("looking for data")

    for tr in more_results:
        all_th_in = tr.find_all("th")

        for th in all_th_in:
            if str(th.text).__contains__("Latest version"):
                all_a_in = tr.find_all("a")

                for a in all_a_in:
                    found.append(a.text + " BE")

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

    logging.info("encoode data")
    return json.JSONEncoder(default=encode_complex, sort_keys=True, indent=4 * ' ', ensure_ascii=False).encode(
        item)


async def be_version_push(json_data):
    logging.info("write file to store")
    f = open(BE_VERSIONS_FILE, "w", encoding='utf-8')
    f.write(json_data)
    f.close()

    file = open(BE_VERSIONS_FILE, 'rb')

    logging.info("stor file to astler.net")
    with ftplib.FTP(FTP_URL, FTP_USER, FTP_PASS) as ftp, file:
        ftp.storbinary(f'STOR /www/astler.net/apps_data/{file.name}', file)

    await send_msg_to_admin(dp, f"Обновлены данные версий BE:\n{json_data}!")
