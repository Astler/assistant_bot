import logging

import requests
import simplejson as json
from bs4 import BeautifulSoup

from cat.utils.ftp_utils import upload_file_to_folder
from cat.utils.json_utils import generate_json_string
from data.config import BE_VERSIONS_FILE
from loader import dp
from utils.notify_admins import send_msg_to_admin


class VersionsItem:
    def __init__(self, release, snapshot):
        self.release = release
        self.snapshot = snapshot

    @classmethod
    def from_dict(cls, data):
        return cls(data['release'], data['snapshot'])

    def __str__(self):
        return f"Release: {self.release}, Snapshot: {self.snapshot}"


class MinecraftVersionsItem:
    be = VersionsItem("", "")
    je = VersionsItem("", "")

    def to_json(self):
        return json.dumps({
            'be': {'release': self.be.release, 'snapshot': self.be.snapshot},
            'je': {'release': self.je.release, 'snapshot': self.je.snapshot}
        })


def fetch_be_versions():
    logging.info("connecting to wiki")
    url = "https://minecraft.fandom.com/wiki/Bedrock_Edition"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup.find_all(class_="pi-data-value")


def fetch_je_versions():
    logging.info("connecting to launchermeta.mojang.com")
    url = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
    response = requests.get(url)

    if response.status_code == 200:
        json_data = response.json()
        latest_versions = json_data['latest']
        return VersionsItem(latest_versions['release'], latest_versions['snapshot'])
    else:
        logging.error(f"Failed to fetch data, status code: {response.status_code}")
        return None


def find_versions(all_lines):
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
        return VersionsItem(found[0], found[1])
    elif len(found) != 0:
        return VersionsItem(found[0], "")

    return VersionsItem("", "")


def encode_complex(obj):
    if isinstance(obj, VersionsItem):
        return {"snapshot": obj.snapshot, "release": obj.release}
    if isinstance(obj, MinecraftVersionsItem):
        return {
            'be': {'release': obj.be.release, 'snapshot': obj.be.snapshot},
            'je': {'release': obj.je.release, 'snapshot': obj.je.snapshot}
        }
    raise TypeError(repr(obj) + " is not JSON serializable")


def save_local_file(json_data):
    logging.info("write file to store")
    with open(BE_VERSIONS_FILE, "w", encoding='utf-8') as f:
        f.write(json_data)


def upload_to_astler_net():
    logging.info("store file to astler.net")
    upload_file_to_folder(BE_VERSIONS_FILE)


async def minecraft_versions_get():
    be_versions = find_versions(fetch_be_versions())
    je_versions = fetch_je_versions()

    minecraft_versions = MinecraftVersionsItem()
    minecraft_versions.be = be_versions
    minecraft_versions.je = je_versions

    json_data = generate_json_string(minecraft_versions, encode_complex)

    return json_data


async def minecraft_version_push(json_data):
    save_local_file(json_data)
    print("save_local_file")
    upload_to_astler_net()
    print("upload_to_astler_net")

    parsed = json.loads(json_data)
    print(parsed)
    be_release = parsed['be']['release']
    be_snapshot = parsed['be']['snapshot']
    je_release = parsed['je']['release']
    je_snapshot = parsed['je']['snapshot']

    await send_msg_to_admin(dp,
                            f"Обновлены данные версий!\n\nBE:\n{be_release} • {be_snapshot}\nJE:\n{je_release} • {je_snapshot}!")
