from aiogram import types
from aiogram.dispatcher.filters import AdminFilter

from bot.filters import IsGroup
from keyboards.base_callback_data import bot_group_settings
from keyboards.bot_settings_group_keyboard import bot_settings_group_keyboard
from loader import dp, bot
from utils.group_data.data import get_group_info, save_group_dict


@dp.message_handler(IsGroup(), AdminFilter(), commands=["settings"])
async def bot_settings_start(message: types.Message):
    chat_id = message.chat.id
    group_settings = get_group_info(chat_id)
    delete_commands = group_settings.delete_commands
    delete_previous_settings = group_settings.delete_previous_settings
    adult_mode = group_settings.adult_mode

    if delete_commands:
        await message.delete()

    msg = await bot.send_message(message.chat.id, "Вот мои текущие настройки!",
                                 reply_markup=bot_settings_group_keyboard(delete_commands, delete_previous_settings,
                                                                          adult_mode))

    if delete_previous_settings:
        settings_msg_last = group_settings.last_settings_msg_id

        group_settings["last_settings_msg_id"] = msg.message_id
        save_group_dict(chat_id, group_settings)

        if settings_msg_last != 0:
            await bot.delete_message(chat_id, settings_msg_last)


@dp.callback_query_handler(AdminFilter(), bot_group_settings.filter(action="toggle_bot_delete_commands"))
async def publish_new_data(query: types.CallbackQuery):
    chat_id = query.message.chat.id
    group_settings = get_group_info(chat_id)
    new_delete_commands_value = not group_settings.delete_commands
    group_settings.delete_commands = new_delete_commands_value
    save_group_dict(chat_id, group_settings)

    delete_commands = group_settings.delete_commands
    delete_previous_settings = group_settings.delete_previous_settings
    adult_mode = group_settings.adult_mode

    if new_delete_commands_value:
        await query.message.edit_text("Теперь бот будет удалять отправленные ему комманды",
                                      reply_markup=bot_settings_group_keyboard(delete_commands,
                                                                               delete_previous_settings, adult_mode))
    else:
        await query.message.edit_text("Теперь бот НЕ будет удалять отправленные ему комманды",
                                      reply_markup=bot_settings_group_keyboard(delete_commands,
                                                                               delete_previous_settings, adult_mode))


@dp.callback_query_handler(AdminFilter(), bot_group_settings.filter(action="toggle_bot_adult_mode"))
async def publish_new_data(query: types.CallbackQuery):
    chat_id = query.message.chat.id
    group_settings = get_group_info(chat_id)
    new_delete_commands_value = not group_settings.adult_mode
    group_settings.adult_mode = new_delete_commands_value
    save_group_dict(chat_id, group_settings)

    delete_commands = group_settings.delete_commands
    delete_previous_settings = group_settings.delete_previous_settings
    adult_mode = group_settings.adult_mode

    if new_delete_commands_value:
        await query.message.edit_text("Теперь в боте доступны злые функции",
                                      reply_markup=bot_settings_group_keyboard(delete_commands,
                                                                               delete_previous_settings, adult_mode))
    else:
        await query.message.edit_text("Теперь бот скроет злые функции",
                                      reply_markup=bot_settings_group_keyboard(delete_commands,
                                                                               delete_previous_settings, adult_mode))


@dp.callback_query_handler(AdminFilter(), bot_group_settings.filter(action="cancel"))
async def publish_new_data(query: types.CallbackQuery):
    await query.message.delete()


@dp.message_handler(IsGroup(), commands=["settings"])
async def bot_settings_start(message: types.Message):
    await message.delete()
