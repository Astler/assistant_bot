import asyncio
import json
import random
from datetime import date

from aiogram import types

from handlers.groups.rep_system_group import create_user_mention, get_cat_user
from loader import dp, app, bot
from utils.group_data.data import get_group_dict, save_group_dict
from utils.group_data.user import CatUser


@dp.message_handler(commands="hero")
async def hero_of_the_day(message: types.Message):
    chat_id = message.chat.id

    group_info = get_group_dict(chat_id)

    members = await app.get_chat_members(message.chat.id)

    all_users_in_chat = []

    for member in members:
        if not member.user.is_bot:
            all_users_in_chat.append(member)

    heroes: dict = group_info.heroes
    users: dict = group_info.users

    today = str(date.today())

    if not heroes.__contains__(today):
        await bot.send_message(message.chat.id, "Провожу опрос общих знакомых")
        await asyncio.sleep(1)
        await bot.send_message(message.chat.id, "Спрашиваю ваших родителей")
        await asyncio.sleep(1)
        await bot.send_message(message.chat.id, "Задаю вопросы усопшим")
        await asyncio.sleep(1)
        await bot.send_message(message.chat.id, "Иду к шаману")
        await asyncio.sleep(1)
        await bot.send_message(message.chat.id, f"Всё, теперь очевидно. Сегодня {group_info.hero_name}...")
        random_user = random.choice(all_users_in_chat)
        user_id = random_user.user.id

        heroes = {today: user_id}

        users[user_id] = json.dumps(get_cat_user(users, user_id).increment_hero_counter(), cls=CatUser.CatUserEncoder)

        await bot.send_message(message.chat.id,
                               f"Это {create_user_mention(await message.bot.get_chat_member(chat_id, user_id))}!",
                               parse_mode="Markdown")
    else:
        user_id = heroes[today]
        await bot.send_message(message.chat.id,
                               f"Сегодняшний ({today}) {group_info.hero_name} уже определён! Это {create_user_mention(await message.bot.get_chat_member(chat_id, user_id))}",
                               parse_mode="Markdown")

    group_info.heroes = heroes
    group_info.users = users

    save_group_dict(chat_id, group_info)
