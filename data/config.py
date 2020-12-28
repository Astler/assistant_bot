import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str("1280483802:AAHNu0JihLQBIZlP1qBsK3pasuNTeFeG7Ns")

if not BOT_TOKEN:
    print('You have forgot to set BOT_TOKEN')
    quit()

HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')

# webhook settings
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{BOT_TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

print(WEBHOOK_URL)

# webserver settings
WEBAPP_HOST = '0.0.0.0'
# WEBAPP_PORT = int(300)
WEBAPP_PORT = 0

if not str(os.getenv('PORT')).__contains__("None"):
    WEBAPP_PORT = int(str(os.getenv('PORT')))

admins = [
    376225089
]

ip = "localhost"

aiogram_redis = {
    'host': ip,
}

redis = {
    'address': (ip, 6379),
    'encoding': 'utf8'
}
