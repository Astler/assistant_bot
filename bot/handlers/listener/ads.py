import asyncio

from aiogram import types

from bot.filters.forward_from_reply import ForwardFromReply
from bot.handlers.listener.data.data import advertisement, add_new_data_to_ads_model, not_advertisement, \
    classify_message_by_model
from cat.utils.telegram_utils import get_message_text
from filters import BotSuperAdminsFilter
from loader import dp


@dp.message_handler(BotSuperAdminsFilter(), ForwardFromReply(), commands=['ads'])
async def cmd_add_to_listener(message: types.Message):
    text = get_message_text(message.reply_to_message)
    await add_new_data_to_ads_model(text, advertisement)

    reply = await message.reply("Message marked as an ad.")
    await message.reply_to_message.delete()
    await message.delete()
    await asyncio.sleep(3)
    await reply.delete()


@dp.message_handler(BotSuperAdminsFilter(), ForwardFromReply(), commands=['not_ads'])
async def cmd_add_to_listener(message: types.Message):
    text = get_message_text(message.reply_to_message)
    await add_new_data_to_ads_model(text, not_advertisement)

    reply = await message.reply("Message marked as an not ad.")
    await message.delete()
    await asyncio.sleep(3)
    await reply.delete()


@dp.message_handler(BotSuperAdminsFilter(), ForwardFromReply(), commands=['check_ads'])
async def cmd_add_to_listener(message: types.Message):
    text = get_message_text(message.reply_to_message)

    category, probabilities = await classify_message_by_model(text)

    await message.reply(f"Category: {category}, Probabilities: {probabilities}")
    print(f"Category: {category}, Probabilities: {probabilities}")
