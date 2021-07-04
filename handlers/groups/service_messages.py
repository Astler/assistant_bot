from aiogram import types

from loader import dp


@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def new_member(m: types.Message):
    members = ", ".join([m.get_mention(as_html=True) for m in m.new_chat_members])
    await m.reply(f"Привет, {members}.")


@dp.message_handler(content_types=types.ContentType.LEFT_CHAT_MEMBER)
async def left_member(m: types.Message):
    if m.from_user.id == m.left_chat_member.id:
        await m.reply(f"{m.left_chat_member.get_mention(as_html=True)} вышел из чата!")
    else:
        await m.reply(
            f"{m.left_chat_member.get_mention(as_html=True)} был удалён пользователем {m.from_user.get_mention(as_html=True)}...")


@dp.message_handler(content_types=types.ContentType.NEW_CHAT_TITLE)
async def new_member(m: types.Message):
    await m.delete()


@dp.message_handler(content_types=types.ContentType.NEW_CHAT_PHOTO)
async def new_member(m: types.Message):
    await m.delete()
