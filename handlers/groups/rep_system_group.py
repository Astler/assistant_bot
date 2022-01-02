import json

from aiogram import types

from filters.is_rep_msg import IsRepMsg
from loader import dp
from utils.group_data.data import get_group_dict, save_group_dict
from utils.group_data.user import CatUser


@dp.message_handler(IsRepMsg())
async def rep_msg(message: types.Message):
    source_message = message.reply_to_message

    if source_message is None:
        return

    chat_id = message.chat.id
    user_id = source_message.from_user.id
    sender_id = message.from_user.id

    if sender_id == user_id:
        if message.text.__contains__("+rep") or message.text.__contains__("+реп"):
            await message.reply("Я тоже себя люблю, но... нет.")
        else:
            await message.reply("Самобичевание не выход D:")
        return

    group_settings = get_group_dict(chat_id)
    print(group_settings)
    users: dict = group_settings.get("users", {})

    if users.__contains__(str(user_id)):
        user_json = users[str(user_id)]
        user = json.loads(user_json, object_hook=lambda d: CatUser(**d))
        print(f"loaded user rep = {user.reputation}")
    else:
        user = CatUser(user_id)

    to_change_user = await message.bot.get_chat_member(chat_id, user_id)
    sender_user = await message.bot.get_chat_member(chat_id, sender_id)

    mention_change_user = "[" + to_change_user.user.username + "](tg://user?id=" + str(user_id) + ")"
    mention_sender_user = "[" + sender_user.user.username + "](tg://user?id=" + str(sender_id) + ")"

    if message.text.__contains__("+rep") or message.text.__contains__("+реп"):
        user.reputation += 1
        await message.reply(
            f"Репутация {mention_change_user} повышена пользователем {mention_sender_user}!\n\nТеперь репутация {mention_change_user} равна: {user.reputation}",
            parse_mode="Markdown")
    else:

        await message.reply(
            f"Репутация {mention_change_user} уменьшена пользователем {mention_sender_user}!\n\nТеперь репутация {mention_change_user} равна: {user.reputation}",
            parse_mode="Markdown")
        user.reputation -= 1

    users[user_id] = json.dumps(user, cls=CatUser.CatUserEncoder)
    group_settings["users"] = users

    save_group_dict(chat_id, group_settings)
