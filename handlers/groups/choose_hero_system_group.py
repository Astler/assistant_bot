import asyncio
import json
import random
from datetime import date

from aiogram import types

from handlers.groups.rep_system_group import create_user_mention, get_cat_user
from loader import dp, bot, app
from utils.group_data.data import get_group_info, save_group_dict
from utils.group_data.user import CatUser


@dp.message_handler(commands=["pidor_stats", "ps"])
async def my_rep(message: types.Message):
    chat_id = message.chat.id

    group_settings = get_group_info(chat_id)
    all_users = group_settings.users

    stats = ""

    for user_id in all_users:
        cat_user: CatUser = json.loads(all_users[user_id], object_hook=lambda d: CatUser(**d))
        try:
            member = await app.get_chat_member(chat_id, cat_user.user_id)
            if not member.user.is_bot:
                stats += f"{create_user_mention(member)} был пидором {cat_user.pidor_times} раз\n"
        except Exception as e:
            print(f"exception {e}")

    await message.reply(stats, parse_mode="Markdown")


@dp.message_handler(commands=["pidor", "p"])
async def my_rep(message: types.Message):
    chat_id = message.chat.id

    group_info = get_group_info(chat_id)

    if not group_info.adult_mode:
        return

    all_in_chat = []

    async for member in app.get_chat_members(message.chat.id):
        if not member.user.is_bot:
            all_in_chat.append(member)

    pidors: dict = group_info.pidors
    users: dict = group_info.users

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
        random_user = random.choice(all_in_chat)
        user_id = random_user.user.id
        pidors[today] = user_id

        users[user_id] = json.dumps(get_cat_user(users, user_id).increment_pidor_counter(), cls=CatUser.CatUserEncoder)

        await bot.send_message(message.chat.id,
                               f"Это {create_user_mention(await message.bot.get_chat_member(chat_id, user_id))}!",
                               parse_mode="Markdown")
    else:
        user_id = pidors[today]
        await bot.send_message(message.chat.id,
                               f"Сегодняшний ({today}) пидор уже определён! Это {create_user_mention(await message.bot.get_chat_member(chat_id, user_id))}",
                               parse_mode="Markdown")

    group_info.users = users
    group_info.pidors = pidors

    save_group_dict(chat_id, group_info)
