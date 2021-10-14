import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TOKEN_KEY")

if not BOT_TOKEN:
    print('You have forgot to set BOT_TOKEN ' + str(BOT_TOKEN) + '?')
    quit()

WEBHOOK_HOST = f'https://catassistantbot.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{BOT_TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = 0

if not str(os.getenv('PORT')).__contains__("None"):
    WEBAPP_PORT = os.getenv('PORT', default=8000)

ADMINS_ENV = os.getenv("ADMINS").split("|")

admins = [int(admin) for admin in ADMINS_ENV]

CHATS_ENV = os.getenv("CHATS").split("|")

chats = [int(admin) for admin in CHATS_ENV]

version = "0.2.1"
