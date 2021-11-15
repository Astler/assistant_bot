from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.keyboard_creation_tools import is_parameter_active


def bot_settings_group_keyboard(
        delete_commands_to_bot: bool,
        delete_previous_settings: bool = False,
):
    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton(f'Удалять комманды бота: {is_parameter_active(delete_commands_to_bot)}',
                                      callback_data="bot_group_settings:toggle_bot_delete_commands"))
    keyboard.add(InlineKeyboardButton(f'Удалять сообщения настроек: {is_parameter_active(delete_previous_settings)}',
                                      callback_data="bot_group_settings:toggle_bot_delete_previous_settings"))
    keyboard.add(InlineKeyboardButton('Отмена', callback_data="bot_group_settings:cancel"))

    return keyboard
