import asyncio
import json
import random
from datetime import date

from aiogram import types

from handlers.groups.rep_system_group import create_user_mention, get_cat_user
from loader import dp, bot, app
from utils.group_data.data import get_group_dict, save_group_dict
from utils.group_data.user import CatUser


@dp.message_handler(commands="all_in_chat")
async def my_rep(message: types.Message):
    members = await app.get_chat_members(message.chat.id)

    all_in_chat = []

    for member in members:
        all_in_chat.append(create_user_mention(member))

    await bot.send_message(message.chat.id, "\n".join(all_in_chat), parse_mode="Markdown")


@dp.message_handler(commands="pidor_stats")
async def my_rep(message: types.Message):
    chat_id = message.chat.id

    group_settings = get_group_dict(chat_id)
    pidors_all = group_settings.get("pidors")

    stats = ""

    for key in pidors_all:
        member = await app.get_chat_member(chat_id, int(pidors_all[key]))
        stats += f"{key} => {create_user_mention(member)}\n"
        print(key)

    await message.reply(stats, parse_mode="Markdown")

    # all_in_chat = []

    # for member in members:
    #     all_in_chat.append(create_user_mention(member))

    # await bot.send_message(message.chat.id, "\n".join(all_in_chat), parse_mode="Markdown")


@dp.message_handler(commands="pidor")
async def my_rep(message: types.Message):
    chat_id = message.chat.id

    group_settings = get_group_dict(chat_id)

    if not group_settings.get("adult_mode", False):
        return

    members = await app.get_chat_members(message.chat.id)

    all_users_in_chat = []

    for member in members:
        if not member.user.is_bot:
            all_users_in_chat.append(member)

    pidors: dict = group_settings.get("pidors", {})
    users: dict = group_settings.get("users", {})

    today = str(date.today())

    if not pidors.__contains__(today):
        await bot.send_message(message.chat.id, "Провожу опрос общих знакомых")
        await asyncio.sleep(1)
        await bot.send_message(message.chat.id, "Спрашиваю ваших родителей")
        await asyncio.sleep(1)
        await bot.send_message(message.chat.id, "Задаю вопросы усопшим")
        await asyncio.sleep(1)
        await bot.send_message(message.chat.id, "Иду к шаману")
        await asyncio.sleep(1)
        await bot.send_message(message.chat.id, "Всё, теперь очевидно. Сегодня пидор...")
        random_user = random.choice(all_users_in_chat)
        user_id = random_user.user.id
        pidors[today] = user_id
        user_to_update = get_cat_user(users, user_id)
        user_to_update.pidor_times += 1
        users[user_id] = json.dumps(user_to_update, cls=CatUser.CatUserEncoder)

        await bot.send_message(message.chat.id,
                               f"Это {create_user_mention(await message.bot.get_chat_member(chat_id, user_id))}!",
                               parse_mode="Markdown")
    else:
        user_id = pidors[today]
        await bot.send_message(message.chat.id,
                               f"Сегодняшний ({today}) пидор уже определён! Это {create_user_mention(await message.bot.get_chat_member(chat_id, user_id))}",
                               parse_mode="Markdown")
        print("PIDR?")

    group_settings["users"] = users
    group_settings["pidors"] = pidors

    save_group_dict(chat_id, group_settings)
