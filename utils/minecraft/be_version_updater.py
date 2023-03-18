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


def fetch_be_versions():
    logging.info("connecting to wiki")
    url = "https://minecraft.fandom.com/wiki/Bedrock_Edition"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup.find_all(class_="pi-data-value")


def find_versions(all_lines):
    item = VersionsItem()
    found = []

    logging.info("looking for data")
    for line in all_lines:
        release_title_check = line.find("b")

        if release_title_check is None:
            continue

        if release_title_check.text != "Release":
            continue

        for a in line.find_all("a"):
            found.append(a.text + " BE")

    if len(found) >= 2:
        item.release = found[0]
        item.snapshot = found[1]
    elif len(found) != 0:
        item.release = found[0]

    return item


def encode_complex(obj):
    if isinstance(obj, VersionsItem):
        return {"snapshot": obj.snapshot, "release": obj.release}
    raise TypeError(repr(obj) + " is not JSON serializable")


def generate_json_string(item):
    logging.info("encode data")
    return json.JSONEncoder(
        default=encode_complex, sort_keys=True, indent=4 * ' ', ensure_ascii=False
    ).encode(item)


def save_local_file(json_data):
    logging.info("write file to store")
    with open(BE_VERSIONS_FILE, "w", encoding='utf-8') as f:
        f.write(json_data)


def upload_to_astler_net():
    logging.info("store file to astler.net")
    with ftplib.FTP(FTP_URL, FTP_USER, FTP_PASS) as ftp, open(BE_VERSIONS_FILE, 'rb') as file:
        ftp.storbinary(f'STOR /www/astler.net/apps_data/{file.name}', file)


async def be_version_get():
    all_lines = fetch_be_versions()
    item = find_versions(all_lines)
    json_data = generate_json_string(item)
    return json_data


async def be_version_push(json_data):
    save_local_file(json_data)
    upload_to_astler_net()
    await send_msg_to_admin(dp, f"Обновлены данные версий BE:\n{json_data}!")