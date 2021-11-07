from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

sticker_keyboard = InlineKeyboardMarkup().row(
    InlineKeyboardButton('Хватит стикеров', callback_data="cancel:cancel")
)

add_channel_keyboard = InlineKeyboardMarkup().row(
    InlineKeyboardButton('Отмена', callback_data="cancel:cancel")
)


def generate_post_keyboard(post_type=""):
    post_keyboard = InlineKeyboardMarkup()

    if post_type == "cancel_edit":
        post_keyboard.add(InlineKeyboardButton('Назад', callback_data="post:edit_text_back"))
        return post_keyboard

    if post_type == "text":
        post_keyboard.add(InlineKeyboardButton('Изменить текст', callback_data="post:edit_text"))
        post_keyboard.add(InlineKeyboardButton('Добавить медиа', callback_data="post:add_img"))
        post_keyboard.add(InlineKeyboardButton('Опубликовать', callback_data="post:publish"))

    if post_type != "":
        post_keyboard.add(
            InlineKeyboardButton(text='Реакции', callback_data="post:add_reaction"),
            InlineKeyboardButton(text='Кнопки', callback_data="post:add_button")
        )

    post_keyboard.add(InlineKeyboardButton('Отмена', callback_data="post:stop"))
    return post_keyboard
