import json
import random
import time
import os

import telebot
from telebot import types
from flask import Flask, request

TOKEN = '957965875:AAGriDg9e0ZR9SbYsqCr3GE3Vu9osC6BDKw'

bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

keyboard_main = types.InlineKeyboardMarkup()
keyboard_main.add(types.InlineKeyboardButton(text='Доступный функционал', callback_data='to_menu_menu'))
keyboard_main.add(types.InlineKeyboardButton(text='Написать автору', callback_data='msg_to_astler'))

keyboard_menu = types.InlineKeyboardMarkup()
keyboard_menu.add(types.InlineKeyboardButton(text='Техническое меню', callback_data='tech_menu'))
keyboard_menu.add(types.InlineKeyboardButton(text='Информационное меню', callback_data='info_menu'))
keyboard_menu.add(types.InlineKeyboardButton(text='Назад', callback_data='to_main_menu'))

keyboard_back_to_main_menu = types.InlineKeyboardMarkup()
keyboard_back_to_main_menu.add(types.InlineKeyboardButton(text='Назад', callback_data='to_main_menu'))

keyboard_back_to_menu_menu = types.InlineKeyboardMarkup()
keyboard_back_to_menu_menu.add(types.InlineKeyboardButton(text='Назад', callback_data='to_menu_menu'))

keyboard_tech = types.InlineKeyboardMarkup()
keyboard_tech.add(types.InlineKeyboardButton(text='Получить ID стикера', callback_data='sticker_get_id'))
keyboard_tech.add(types.InlineKeyboardButton(text='Назад', callback_data='to_menu_menu'))


@bot.message_handler(content_types=['sticker'])
def sticker_msg(message):
    bot.reply_to(message, message)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_sticker(message.from_user.id, 'CAADAgADlgADIIAaIgm1NCRfWlNpFgQ')
    msg = 'Привет, ' + message.from_user.first_name + '!'
    bot.send_message(message.from_user.id, msg)
    bot.send_message(message.from_user.id, text='Что делаем сегодня?', reply_markup=keyboard_main)


lol_stickers = {
    1: 'CAADAgADggADIIAaInrRz2SwfUDhFgQ',
    2: 'CAADAgADewADIIAaItT5K2jhxWrMFgQ',
    3: 'CAADAgADegADIIAaIv90h7zb0DkTFgQ'
}


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    lowerText = str(message.text).lower()
    if lowerText == "меню" or lowerText == "menu":
        bot.send_sticker(message.from_user.id, "CAADAgADnQADIIAaIo5Vgyzp5HU0FgQ")
        bot.send_message(message.from_user.id, text='Слушаю...', reply_markup=keyboard_main)
    elif lowerText == "смех" or lowerText == "lol" or lowerText == "лол":
        rand_lol = lol_stickers[random.randint(1, 3)]
        bot.send_sticker(message.from_user.id, rand_lol)
    elif message.text == "/help":
        bot.send_sticker(message.from_user.id, "CAADAgADkQADIIAaInNnqBJmYzqtFgQ")
        bot.send_message(message.from_user.id, text='Нужна помощь? С чем? Такс, ладно, все, что я пока могу — можешь '
                                                    'увидеть тут. Это же меню можно вызвать в любое время написав '
                                                    'слово Меню (можно меню, menu). Обращайся)',
                         reply_markup=keyboard_main)
    elif message.text == "Пока":
        bot.send_sticker(message.from_user.id, "CAADAgADeAADIIAaIgUnNYxeyPi0FgQ")
    elif lowerText == "даша":
        bot.send_sticker(message.from_user.id, "CAADAgADegADIIAaIv90h7zb0DkTFgQ")
    elif message.text == "Иди в жопу":
        bot.send_sticker(message.from_user.id, "CAADAgADiAADIIAaIocwc0MVqHIzFgQ")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "academy":
        msg = 'Я пока не получил сводок... Попробуем позже?'
        bot.send_message(call.message.chat.id, msg)
    elif call.data == "sticker_get_id":
        bot.send_sticker(call.message.chat.id, "CAADAgADmgADIIAaIhKT3a71KPuVFgQ")
        msg = bot.send_message(call.message.chat.id, "Кидай свой стикер...")
        bot.register_next_step_handler(msg, sticker_id_reply)
    elif call.data == "msg_to_astler":
        bot.send_sticker(call.message.chat.id, "CAADAgADlwADIIAaIhOSoYn7H8VvFgQ")
        bot.send_message(call.message.chat.id, text='Пиши ^_^ @Astler', reply_markup=keyboard_back_to_main_menu)
    elif call.data == "tech_menu":
        bot.send_sticker(call.message.chat.id, "CAADAgADhAADIIAaIin7o9E4IgEiFgQ")
        bot.send_message(call.message.chat.id, text='Мы сотворим великие дела!', reply_markup=keyboard_tech)
    elif call.data == "info_menu":
        bot.send_sticker(call.message.chat.id, "CAADAgADmQADIIAaIm0iFncDb2l8FgQ")
        bot.send_message(call.message.chat.id, text='Тут будет что-то скоро, но автор был слишком занят...',
                         reply_markup=keyboard_back_to_menu_menu)
    elif call.data == "to_main_menu":
        bot.clear_step_handler(call.message)
        bot.send_sticker(call.message.chat.id, "CAADAgADnQADIIAaIo5Vgyzp5HU0FgQ")
        bot.send_message(call.message.chat.id, text='Слушаю...', reply_markup=keyboard_main)
    elif call.data == "to_menu_menu":
        bot.clear_step_handler(call.message)
        bot.send_sticker(call.message.chat.id, "CAADAgADhQADIIAaInGPMZyAFM_yFgQ")
        bot.send_message(call.message.chat.id, text='Ну я пока бот в развитии, так что многого не жди...',
                         reply_markup=keyboard_menu)


def sticker_id_reply(message):
    msg_text = str(message).strip("'<>() ").replace('\'', '\"').replace('False', 'false').replace('None',
                                                                                                  'false').replace(
        'True', 'true').replace('<', '\"').replace('>', '\"')
    json_string = json.loads(msg_text)

    if json_string['sticker']:
        keyboard_another_sticker = types.InlineKeyboardMarkup()
        keyboard_another_sticker.add(types.InlineKeyboardButton(text='Да!', callback_data='sticker_get_id'))
        keyboard_another_sticker.add(types.InlineKeyboardButton(text='Не, назад', callback_data='to_menu_menu'))
        bot.reply_to(message, json_string['sticker']['file_id'])
        bot.send_message(message.chat.id, text='Есть еще стикеры для меня?', reply_markup=keyboard_another_sticker)
    else:
        bot.reply_to(message, "Это явно не стикер!")
        msg = bot.send_message(message.chat.id, "Попробуем снова. Кидай свой стикер...")
        bot.register_next_step_handler(msg, sticker_id_reply)
        bot.send_message(message.chat.id, text='В предыдущее меню', reply_markup=keyboard_back_to_main_menu)


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

while True:
    try:
        bot.polling(none_stop=True)
    except Exception:
        time.sleep(15)
