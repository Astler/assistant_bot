import random
import apiai, json

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, BaseFilter

import logging

TOKEN = "idk"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher


class OrFilter(BaseFilter):
    def filter(self, message):
        lowerText = str(message.text).lower()
        return lowerText.__contains__('или') & lowerText.startswith("эш")


class WhoIsFilter(BaseFilter):
    def filter(self, message):
        lowerText = str(message.text).lower()
        return (lowerText.__contains__('кто сегодня') | lowerText.__contains__('кто у нас')) & lowerText.startswith(
            "эш")


class AsheFilter(BaseFilter):
    def filter(self, message):
        lowerText = str(message.text).lower()
        return lowerText.startswith('эш')


def start(update, context):
    keyboard = [[InlineKeyboardButton("Option 1", callback_data='to_menu_menu'),
                 InlineKeyboardButton("Option 2", callback_data='2')],
                [InlineKeyboardButton("Option 3", callback_data='3')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    msg = 'Привет, ' + update.message.from_user.first_name + '!'
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Что делаем сегодня?', reply_markup=reply_markup)


def textMessage(update, context):
    request = apiai.ApiAI('438ebccebab24fe08d804941ee70934b').text_request()  # Токен API к Dialogflow
    request.lang = 'ru'  # На каком языке будет послан запрос
    request.session_id = 'AstlerAssistantAIBot'  # ID Сессии диалога (нужно, чтобы потом учить бота)
    request.query = update.message.text  # Посылаем запрос к ИИ с сообщением от юзера
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech']  # Разбираем JSON и вытаскиваем ответ
    # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
    if response:
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Я Вас не совсем понял!')


def caps(update, context):
    print(context.args)
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def orMessage(update, context):
    msg = str(update.message.text)

    msg = msg[2:].replace("?", "")

    variants_array = msg.split(" или ")

    for index, variant in enumerate(variants_array):
        while variant.startswith(" ") | variant.startswith(","):
            variant = variant[1:]

        variants_array[index] = variant

    answer = variants_array[random.randint(0, len(variants_array) - 1)]

    context.bot.send_message(chat_id=update.effective_chat.id, text=answer)


def whoIsMessage(update, context):
    msg = str(update.message.text)

    msg = msg[2:].replace("?", "").replace(" кто сегодня ", "").replace(" кто у нас ", "")

    while msg.startswith(" ") | msg.startswith(",") | msg.startswith("."):
        msg = msg[1:]

    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


def button(update, context):
    query = update.callback_query

    query.answer()

    query.edit_message_text(text="Selected option: {}".format(query.data))


# Хендлеры

filter_awesome = AsheFilter()
or_filter = OrFilter()
who_is_filter = WhoIsFilter()

start_handler = CommandHandler('start', start)
caps_handler = CommandHandler('caps', caps)
ai_handler = MessageHandler(filter_awesome, textMessage)
or_handler = MessageHandler(or_filter, orMessage)
who_is_handler = MessageHandler(who_is_filter, whoIsMessage)
#echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(caps_handler)
# dispatcher.add_handler(ai_handler)
dispatcher.add_handler(or_handler)
dispatcher.add_handler(who_is_handler)
#dispatcher.add_handler(echo_handler)
dispatcher.add_handler(CallbackQueryHandler(button))

updater.start_polling()

print("idle")

updater.idle()
