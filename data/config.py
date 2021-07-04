import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str("1825832213:AAGjVCLBcw_AZynaiU2fuZVs6O8ykJr4W5A")

if not BOT_TOKEN:
    print('You have forgot to set BOT_TOKEN')
    quit()

HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')

# webhook settings
WEBHOOK_HOST = f'https://catassistantbot.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{BOT_TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

print(WEBHOOK_URL)

WEBAPP_HOST = '0.0.0.0'
# WEBAPP_PORT = int(300)
WEBAPP_PORT = 0

if not str(os.getenv('PORT')).__contains__("None"):
    WEBAPP_PORT = os.getenv('PORT', default=8000)

admins = [
    376225089
]

myChats = [
    -1001496194797
]

ip = "localhost"

aiogram_redis = {
    'host': ip,
}

redis = {
    'address': (ip, 6379),
    'encoding': 'utf8'
}
