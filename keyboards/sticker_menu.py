from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

sticker_keyboard = InlineKeyboardMarkup().row(
    InlineKeyboardButton('Хватит стикеров', callback_data="sticker:stop")
)
