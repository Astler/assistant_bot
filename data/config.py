import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TOKEN_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN_KEY")
GITHUB_REPO = os.getenv("GITHUB_REPO")

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

version = "0.2.7"


LINKS_BLACK_LIST_ENV = os.getenv("LINKS_BLACK_LIST").split("|")

links_black_list = [
    "astler.test"
]

links_black_list.extend(LINKS_BLACK_LIST_ENV)

changes = """Изменения
0.2-0.2.2 - Удалил лишнее, поправил троттлер
0.2.3 - Добавил чёрный список текста (ссылок), который подлежит удалению. Добавлять можно как через .env 
LINKS_BLACK_LIST, так и в config.py 
0.2.4 - Обновил сервисное новых пользователей в группе, чтобы бот не приветствовал сам себя
0.2.5 - Добавил заглушки в группу для команд, которые предназначены для ЛС
Обновил help, start + добавил отдельный вариант для групп
Добавил топорное сохранение данных
Добавил команду для получения айдишников стикеров, в т.ч. инлайн меню
0.2.5.1 - Исправил баг, при котором не удалялось техническое сообщение (link_spam_group.py) при удалении сообщения триггера кем-то другим
0.2.6 - Обновил функции редактирования канала: set_title, set_photo, set_description
0.2.6.1 - Теперь оповещение о спаме сообщает и канал, где было заблокированно сообщение
0.2.7 - Т.к. Файловая система Heroku эфемерна и стирается при каждом перезапуске, то теперь файлики юзеров загружаются на гитхам 🤣
"""