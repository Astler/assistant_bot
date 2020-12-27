import random
import logging
import random
from abc import ABCMeta
from typing import Optional, Union, Dict

import apiai
import json
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, BaseFilter
from telethon.sync import TelegramClient

api_id = 1381554
api_hash = '4dfa4e1a4c4fa9b6f0b2dcbf157ad60e'

TOKEN = '1280483802:AAHNu0JihLQBIZlP1qBsK3pasuNTeFeG7Ns'

client = TelegramClient('bot', api_id, api_hash).start(bot_token=TOKEN)

if not client.is_user_authorized():
    client.send_code_request(TOKEN)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
jobs = updater.job_queue


class OrFilter(BaseFilter, metaclass=ABCMeta):
    def __call__(self, update: Update) -> Optional[Union[bool, Dict]]:
        pass

    def filter(self, message):
        lowerText = str(message.text).lower()
        return lowerText.__contains__('или') & lowerText.startswith("эш")


class WhoIsFilter(BaseFilter, metaclass=ABCMeta):
    def __call__(self, update: Update) -> Optional[Union[bool, Dict]]:
        pass

    def filter(self, message):
        lowerText = str(message.text).lower()
        return (lowerText.__contains__('кто сегодня')) & lowerText.startswith(
            "эш")


class AsheFilter(BaseFilter):
    def __call__(self, update: Update) -> Optional[Union[bool, Dict]]:
        pass

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
    client.loop.run_until_complete(getUsers(context, update))


async def getUsers(context, update):
    msg = str(update.message.text)
    id = update.effective_chat.id
    print("inside " + str(id))

    entity = await client.get_entity(id)
    users = client.get_participants(entity)

    users = await users

    usersIds = []

    for i in users:
        userId = ""

        print(i.username)
        print(i.username != "None")

        userName = str(i.username)

        if userName != "None":
            userId = "@" + userName
        else:
            print(i.first_name)
            if str(i.first_name) != "None":
                userId += i.first_name

            if str(i.last_name) != "None":
                userId += " " + str(i.last_name)

        usersIds.append(userId)
        print(i.id, i.username, i.first_name, i.last_name)

    msg = msg[2:].replace("?", "").replace(" кто ", "")

    while msg.startswith(" ") | msg.startswith(",") | msg.startswith("."):
        msg = msg[1:]

    answer = usersIds[random.randint(0, len(usersIds) - 1)]

    msg = answer + " " + msg

    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


def button(update, context):
    query = update.callback_query

    query.answer()

    query.edit_message_text(text="Selected option: {}".format(query.data))


def textFormat(update, context):
    print("WHA?")
    print(str(context.args))

    arguments = context.args

    for index, element in enumerate(arguments):
        textElement = str(element)

        if textElement == "-":
            arguments[index] = '—'
        elif (len(textElement) == 2 or len(textElement) == 3) and textElement.endswith("2"):
            arguments[index] = textElement[:-1] + "²"
        elif textElement.startswith(","):
            arguments[index] = ", " + textElement[1:]
        elif textElement.startswith("."):
            arguments[index] = ". " + textElement[1:]
        elif textElement == "1/4":
            arguments[index] = "¼"

    text_formatted_text = ' '.join(arguments)

    text_formatted_text = text_formatted_text.replace(" ,", ",").replace(" .", ".").replace("(c)", "©").replace("(r)", "®")

    context.bot.send_message(chat_id=update.effective_chat.id, text=text_formatted_text)


def callback_30(context):
    print("hi")


jobs.run_once(callback_30, 30)

# Хендлеры

filter_awesome = AsheFilter()
or_filter = OrFilter()
who_is_filter = WhoIsFilter()

start_handler = CommandHandler('start', start)
caps_handler = CommandHandler('caps', caps)
text_format_handler = CommandHandler('f', textFormat)
ai_handler = MessageHandler(filter_awesome, textMessage)
or_handler = MessageHandler(or_filter, orMessage)
who_is_handler = MessageHandler(who_is_filter, whoIsMessage)
# echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(caps_handler)
dispatcher.add_handler(text_format_handler)
# dispatcher.add_handler(ai_handler)
dispatcher.add_handler(or_handler)
dispatcher.add_handler(who_is_handler)
# dispatcher.add_handler(echo_handler)
dispatcher.add_handler(CallbackQueryHandler(button))

updater.start_polling()

updater.idle()
