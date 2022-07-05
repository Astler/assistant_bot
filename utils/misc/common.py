import time
from aiogram.types import ChatMember


def time_in_millis():
    return round(time.time() * 1000)


def create_user_mention(chat_member: ChatMember):
    user_name = chat_member.user.username

    if user_name is None:
        user_name = chat_member.user.first_name

    return "[" + user_name + "](tg://user?id=" + str(chat_member.user.id) + ")"
