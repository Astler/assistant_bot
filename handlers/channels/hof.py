import asyncio
import json
import urllib.request

from aiogram import types

from filters.my_chat_filter import MyChatFilter
from loader import dp


@dp.message_handler(MyChatFilter(), commands="hof")
async def bot_get_hof(message: types.Message):
    text = "Загрузка данных..."

    msg = await message.answer(text)
    await asyncio.sleep(1)

    with urllib.request.urlopen("https://geekstand.top/hof.json") as url:
        data = url.read().decode()

        json_users = json.loads(data)

        await msg.edit_text(text)

        for item in json_users['mUsers']:
            nUserInfo = item['mName'] + "\n\n"
            if item['mDescription'] == "id_developer":
                nUserInfo += "Разработчик (Сосдатель)"
            else:
                nUserInfo += item['mDescription']

            text += "\n\n • " + nUserInfo

        await msg.edit_text(text)
        await message.answer("Обращайся!")


@dp.message_handler(MyChatFilter(), commands="mlv")
async def bot_echo(message: types.Message):
    answer = await message.answer("Так, ищем версию... ")
    with urllib.request.urlopen("https://launchermeta.mojang.com/mc/game/version_manifest.json") as url:
        data = url.read().decode()

        versions = json.loads(data)

        latest = versions['latest']

        release = latest['release']
        snapshot = latest['snapshot']

        text = f"Последняя релизная версия: {release}, а снапшот: {snapshot}."
        await answer.edit_text(text)
