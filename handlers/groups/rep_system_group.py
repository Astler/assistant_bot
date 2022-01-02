import json

from aiogram import types

from filters.is_rep_msg import IsRepMsg, positive_rep
from loader import dp
from utils.group_data.data import get_group_dict, save_group_dict
from utils.group_data.user import CatUser


@dp.message_handler(IsRepMsg())
async def rep_msg(message: types.Message):
    source_message = message.reply_to_message

    if source_message is None:
        return

    chat_id = message.chat.id
    user_to_update_id = source_message.from_user.id
    user_change_author_id = message.from_user.id

    if user_change_author_id == user_to_update_id:
        if any(word in message.text for word in positive_rep):
            await message.reply("Я тоже себя люблю, но... нет.")
        else:
            await message.reply("Самобичевание не выход D:")
        return

    group_settings = get_group_dict(chat_id)
    users: dict = group_settings.get("users", {})

    if users.__contains__(str(user_to_update_id)):
        user_json = users[str(user_to_update_id)]
        user_to_update = json.loads(user_json, object_hook=lambda d: CatUser(**d))
    else:
        user_to_update = CatUser(user_to_update_id)

    if users.__contains__(str(user_change_author_id)):
        user_json = users[str(user_change_author_id)]
        user_change_author = json.loads(user_json, object_hook=lambda d: CatUser(**d))
    else:
        user_change_author = CatUser(user_to_update_id)

    to_change_user = await message.bot.get_chat_member(chat_id, user_to_update_id)
    sender_user = await message.bot.get_chat_member(chat_id, user_change_author_id)

    mention_change_user = "[" + to_change_user.user.username + "](tg://user?id=" + str(user_to_update_id) + ")"
    mention_sender_user = "[" + sender_user.user.username + "](tg://user?id=" + str(user_change_author_id) + ")"

    if any(word in message.text for word in positive_rep):
        user_to_update.reputation += 1
        await message.reply(
            f"Репутация {mention_change_user}  *{user_to_update.reputation}* ❤  повышена пользователем {mention_sender_user}  *{user_change_author.reputation}* ❤  !",
            parse_mode="Markdown")

    else:
        user_to_update.reputation -= 1
        await message.reply(
            f"Репутация {mention_change_user}  *{user_to_update.reputation}* ❤  уменьшена пользователем {mention_sender_user}  *{user_change_author.reputation}* ❤  !",
            parse_mode="Markdown")

    users[user_to_update_id] = json.dumps(user_to_update, cls=CatUser.CatUserEncoder)
    group_settings["users"] = users

    save_group_dict(chat_id, group_settings)
