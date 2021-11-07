import asyncio

from aiogram import types

from data.config import admins, links_black_list
from filters import IsGroup
from loader import dp

from utils.group_data.data import get_group_file, get_group_dict, get_blocked_links, save_group_dict

@dp.message_handler(IsGroup())
async def spam_links_msg(message: types.Message):
    text = message.text

    check_links = links_black_list

    check_links.extend(get_blocked_links(message.chat.id))

    if any(bl_url in text for bl_url in links_black_list):
        info_msg = await message.bot.send_message(message.chat.id,
                                                  "На этом канале запрещены ссылки, скрывающие реальный адрес "
                                                  "вебсайта. Если это сообщение получено по ошибке - обратитесь"
                                                  " к администрации.")
        try:
            await message.delete()
        except Exception as e:
            print(f"Сообщение удалено кем-то другим! {e}")

        [await message.bot.send_message(admin_chat, f"Я удалил сообщение!\n\n"
                                                    f"Чат: {message.chat.title}\n"
                                                    f"Отправитель: {message.from_user.full_name}\n"
                                                    f"Id Отправителя: {message.from_user.id}\n"
                                                    f"Текст: {text}") for admin_chat in admins]

        await asyncio.sleep(10)

        await info_msg.delete()
