import asyncio

from aiogram import types

from data.config import links_black_list
from loader import dp


@dp.message_handler()
async def spam_links_msg(message: types.Message):
    text = message.text

    if any(bl_url in text for bl_url in links_black_list):
        info_msg = await message.bot.send_message(message.chat.id, "Что? Думаю, что это лучше удалить...")
        await message.delete()
        await asyncio.sleep(5)
        await info_msg.delete()
