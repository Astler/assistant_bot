# import json
#
# from aiogram import types
# from apiai import apiai
#
# from loader import dp
#
#
# @dp.message_handler()
# async def bot_echo(message: types.Message):
#     request = apiai.ApiAI('cat-project-acd10').text_request()  # Токен API к Dialogflow
#     request.lang = 'ru'  # На каком языке будет послан запрос
#     request.session_id = 'BatlabAIBot'  # ID Сессии диалога (нужно, чтобы потом учить бота)
#     request.query = message.text  # Посылаем запрос к ИИ с сообщением от юзера
#
#     responseJson = json.loads(request.getresponse().read().decode('utf-8'))
#
#     print(responseJson)
#
#     response = responseJson['result']['fulfillment']['speech']  # Разбираем JSON и вытаскиваем ответ
#     # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
#     if response:
#         dp.bot.send_message(chat_id=message.chat.id, text=response)
#     else:
#         dp.bot.send_message(chat_id=message.chat.id, text='Я Вас не совсем понял!')
