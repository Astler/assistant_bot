import re

from aiogram import types
from aiogram.dispatcher.filters import AdminFilter

from filters import IsGroup
from keyboards.base_callback_data import bot_group_settings
from keyboards.bot_settings_group_keyboard import bot_settings_group_keyboard
from loader import dp, bot

from utils.group_data.data import get_group_dict, get_blocked_links, save_group_dict, get_delete_commands, \
    get_last_settings_msg


@dp.message_handler(IsGroup(), AdminFilter(), commands=["settings"])
async def bot_settings_start(message: types.Message):
    chat_id = message.chat.id
    group_settings = get_group_dict(chat_id)
    delete_commands = group_settings.get("delete_commands", True)
    delete_previous_settings = group_settings.get("delete_previous_settings", True)

    if delete_commands:
        await message.delete()

    msg = await bot.send_message(message.chat.id, "Вот мои текущие настройки!",
                                 reply_markup=bot_settings_group_keyboard(delete_commands, delete_previous_settings))

    if delete_previous_settings:
        settings_msg_last = group_settings.get("last_settings_msg_id", 0)

        group_settings["last_settings_msg_id"] = msg.message_id
        save_group_dict(chat_id, group_settings)

        if settings_msg_last != 0:
            await bot.delete_message(chat_id, settings_msg_last)


@dp.callback_query_handler(AdminFilter(), bot_group_settings.filter(action="toggle_bot_delete_commands"))
async def publish_new_data(query: types.CallbackQuery):
    chat_id = query.message.chat.id
    group_settings = get_group_dict(chat_id)
    new_delete_commands_value = not group_settings.get("delete_commands", True)
    group_settings["delete_commands"] = new_delete_commands_value
    save_group_dict(chat_id, group_settings)

    if new_delete_commands_value:
        await query.message.edit_text("Теперь бот будет удалять отправленные ему комманды",
                                      reply_markup=bot_settings_group_keyboard(new_delete_commands_value))
    else:
        await query.message.edit_text("Теперь бот НЕ будет удалять отправленные ему комманды",
                                      reply_markup=bot_settings_group_keyboard(new_delete_commands_value))


@dp.callback_query_handler(AdminFilter(), bot_group_settings.filter(action="cancel"))
async def publish_new_data(query: types.CallbackQuery):
    await query.message.delete()


@dp.message_handler(IsGroup(), commands=["settings"])
async def bot_settings_start(message: types.Message):
    await message.delete()
