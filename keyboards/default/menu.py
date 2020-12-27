from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Ошибка/Сбой")
        ],
        [
            KeyboardButton(text="Идея"),
            KeyboardButton(text="Помощь")
        ]
    ],
    resize_keyboard=True
)
