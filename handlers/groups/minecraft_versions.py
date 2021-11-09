import json
import urllib.request

from aiogram import types

from data.config import APPS_DATA_ROOT_URL, BE_VERSIONS_FILE
from filters import IsGroup
from keyboards.minecraft_keyboards import minecraft_versions_keyboard
from loader import dp


@dp.message_handler(IsGroup(), commands="minecraft_versions")
async def bot_echo(message: types.Message):
    answer = await message.answer("Так, ищем версию... ")

    versions_dict = {}

    text = ""
    with urllib.request.urlopen("https://launchermeta.mojang.com/mc/game/version_manifest.json") as url:
        data = url.read().decode()

        versions = json.loads(data)

        latest = versions['latest']

        release = latest['release']
        snapshot = latest['snapshot']

        versions_dict[f"{release} JE"] = release
        versions_dict[f"{snapshot} JE"] = snapshot

        text += f"Последняя релизная версия JE: {release}, а снапшот: {snapshot}."

    with urllib.request.urlopen(APPS_DATA_ROOT_URL + BE_VERSIONS_FILE) as url:
        data = url.read().decode()

        versions = json.loads(data)

        release_raw = versions['release']
        snapshot_raw = versions['snapshot']

        release = str(release_raw).replace("_(Bedrock_Edition)", "")
        snapshot = str(snapshot_raw).replace("_(Bedrock_Edition)", "")

        versions_dict[f"{release} BE"] = release_raw
        versions_dict[f"{snapshot} BE"] = snapshot_raw

        text += f"\n\nПоследняя релизная версия BE: {release}, а снапшот: {snapshot}."

    await answer.edit_text(text, reply_markup=minecraft_versions_keyboard(versions_dict))
