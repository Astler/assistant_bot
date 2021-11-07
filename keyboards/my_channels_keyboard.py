from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def generate_user_channels_keyboard(channels_list: dict):
    keyboard = InlineKeyboardMarkup()

    for channel_url in channels_list:
        keyboard.add(InlineKeyboardButton(channels_list[channel_url], url=channel_url))

    return keyboard
