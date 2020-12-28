from aiogram import types

from loader import dp
from filters import IsPrivate, IsGroup

from data.config import admins

import urllib.request

import json


@dp.message_handler(IsGroup(), commands="hof")
async def bot_get_hof(message: types.Message):
    await message.answer("Кого-то тут нет. Как думаешь? Да...Элизаб...Каледония Эш! Легенда преступного мира.")

    with urllib.request.urlopen("https://geekstand.top/hof.json") as url:
        data = json.loads(url.read().decode())

        json_array = json.load(data)
        store_list = []

        for item in json_array:
            store_details = {'mName': item['mName'], 'mDescription': item['mDescription']}
            store_list.append(store_details)

        await message.answer(str(store_list))


@dp.message_handler(commands="secret", user_id=admins)
async def bot_echo(message: types.Message):
    await message.answer("Вы имеете доступ к секретному разделу!")


@dp.message_handler(text="лепи")
async def bot_wtf(message: types.Message):
    await message.answer("Леха пидор!")
