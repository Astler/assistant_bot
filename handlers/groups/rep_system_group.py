import json

from aiogram import types

from bot.filters.reputation_filter import ReputationFilter, positive_rep_keywords
from loader import dp
from utils.group_data.data import get_group_info, save_group_dict, get_cat_user
from utils.group_data.user import CatUser
from utils.misc.common import time_in_millis, create_user_mention


@dp.message_handler(commands=["my_rep", "mr"])
async def my_rep(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    group_settings = get_group_info(chat_id)

    cat_user_info = get_cat_user(group_settings.users, user_id)

    is_adult_mode = group_settings.adult_mode

    mention_user = create_user_mention(await message.bot.get_chat_member(chat_id, user_id))

    user_info_text = f"""Привет, {mention_user}!
    
    Твоя репутация в этом чате: *{cat_user_info.reputation}* ❤"""

    if is_adult_mode:
        user_info_text += f"\nТы был пидором {cat_user_info.pidor_times} раз"

    await message.reply(user_info_text, parse_mode="Markdown")


@dp.message_handler(commands=["group_rep", "gr"])
async def group_rep(message: types.Message):
    chat_id = message.chat.id

    group_settings = get_group_info(chat_id)
    users: dict = group_settings.users

    users_by_rep = {}

    for user in users:
        cat_user_info = get_cat_user(users, user)
        users_by_rep[cat_user_info.user_id] = cat_user_info.reputation

    dict(sorted(users_by_rep.items(), key=lambda item: item[1]))

    users_with_rep = []

    for user_id in users_by_rep.keys():
        mention_user = create_user_mention(await message.bot.get_chat_member(chat_id, user_id))
        users_with_rep.append(f"{mention_user}: *{users_by_rep[user_id]}* ❤")

    await message.reply("\n".join(users_with_rep), parse_mode="Markdown")


@dp.message_handler(ReputationFilter())
async def rep_msg(message: types.Message):
    source_message = message.reply_to_message

    if source_message is None:
        return

    chat_id = message.chat.id
    user_to_update_id = source_message.from_user.id
    user_change_author_id = message.from_user.id

    if user_change_author_id == user_to_update_id:
        await rep_change_for_self(message)
        return

    group_settings = get_group_info(chat_id)
    users: dict = group_settings.users

    user_to_update = get_cat_user(users, user_to_update_id)
    user_change_author = get_cat_user(users, user_change_author_id)

    if user_change_author.last_rep_edit_time != 0 and time_in_millis() - user_change_author.last_rep_edit_time < 30000:
        await message.reply("Слишком часто менять репутацию нельзя!")
        return

    user_change_author.last_rep_edit_time = time_in_millis()

    mention_change_user = create_user_mention(await message.bot.get_chat_member(chat_id, user_to_update_id))
    mention_sender_user = create_user_mention(await message.bot.get_chat_member(chat_id, user_change_author_id))

    if any(word in message.text for word in positive_rep_keywords) or str(message.text) == "+" or str(
            message.text) == "➕" or str(message.text) == "❤":
        user_to_update.reputation += 1
        await message.reply(
            f"Репутация {mention_change_user} *{user_to_update.reputation}* ❤ повышена пользователем {mention_sender_user} *{user_change_author.reputation}* ❤ !",
            parse_mode="Markdown")
    else:
        user_to_update.reputation -= 1
        await message.reply(
            f"Репутация {mention_change_user} *{user_to_update.reputation}* ❤ уменьшена пользователем {mention_sender_user} *{user_change_author.reputation}* ❤ !",
            parse_mode="Markdown")

    users[user_to_update_id] = json.dumps(user_to_update, cls=CatUser.CatUserEncoder)
    users[user_change_author_id] = json.dumps(user_change_author, cls=CatUser.CatUserEncoder)
    group_settings.users = users

    save_group_dict(chat_id, group_settings)


async def rep_change_for_self(message: types.Message):
    if any(word in message.text for word in positive_rep_keywords):
        await message.reply("Я тоже себя люблю, но... нет.")
    else:
        await message.reply("Самобичевание не выход D:")


