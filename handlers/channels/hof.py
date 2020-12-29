import asyncio
import json
import urllib.request

from aiogram import types

from data.config import admins
from loader import dp


@dp.message_handler(commands="hof")
async def bot_get_hof(message: types.Message):
    text = "Кого-то тут нет. БОБ! Как думаешь? Да...Элизаб...Каледония Эш! Легенда преступного мира..?"
    msg = await message.answer(text)
    await asyncio.sleep(1)

    with urllib.request.urlopen("https://geekstand.top/hof.json") as url:
        data = url.read().decode()

        json_users = json.loads(data)

        text = "Да, список почти готов. Буквально последние штрихи"
        await msg.edit_text(text)

        await asyncio.sleep(1)

        text = "Вот теперь это можно и людям показать!"
        await msg.edit_text(text)
        await asyncio.sleep(1)
        text += "\n\nЗал славы сообщества KB!"
        await msg.edit_text(text)
        text += "Элизабет Каледония Эш\n\nЛегендарный главарь Банды Мертвецов, крайне полезный бот."
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


@dp.message_handler(commands="mlv")
async def bot_echo(message: types.Message):
    text = "Думаешь там что-то изменилось с прошлого раза? "
    answer = await message.answer("Думаешь там что-то изменилось с прошлого раза? ")
    with urllib.request.urlopen("https://launchermeta.mojang.com/mc/game/version_manifest.json") as url:
        data = url.read().decode()

        versions = json.loads(data)

        latest = versions['latest']

        release = latest['release']
        snapshot = latest['snapshot']
        text += f"\n\nПоследняя релизная версия так и осталась {release}, а снапшот {snapshot}."
        await answer.edit_text(text)

        await message.answer("Может тебе ещё ссылку на скачивание на блюдечке принести?")


@dp.message_handler(text="Хорошко")
async def bot_wtf(message: types.Message):
    await message.answer("Бррр... Зачем ты его вспонил?!")
