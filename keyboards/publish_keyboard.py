from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def publish_keyboard():
    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton('Опубликовать', callback_data="callback:publish"))
    keyboard.add(InlineKeyboardButton('Отмена', callback_data="callback:cancel"))

    return keyboard


def check_keyboard(url):
    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton('Проверить данные', url=url))

    return keyboard

