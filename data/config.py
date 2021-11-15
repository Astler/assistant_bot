import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TOKEN_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN_KEY")
GITHUB_REPO = os.getenv("GITHUB_REPO")
A_PATH = os.getenv('A_PATH')

FTP_URL = os.getenv('FTP_URL')
FTP_USER = os.getenv('FTP_USER')
FTP_PASS = os.getenv('FTP_PASS')

BANNERS_MAP_FILE = os.getenv('BANNERS_MAP_FILE')
BE_VERSIONS_FILE = os.getenv('BE_VERSIONS_FILE')
APPS_DATA_ROOT_URL = os.getenv('APPS_DATA_ROOT_URL')

######
# FB #
######

CERT_PATH = os.getenv('CERT_PATH')
PROJECT_ID = os.getenv('PROJECT_ID')

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

CHATS_ENV = os.getenv("CHATS").split("|")

chats = [int(admin) for admin in CHATS_ENV]

version = "0.3.2"

LINKS_BLACK_LIST_ENV = os.getenv("LINKS_BLACK_LIST")

links_black_list = [
    "astler.test",
    "cutt.ly",
    "cutt.us",
    "tinyurl.com",
    "cuti.cc",
    "gee.su",
]

if LINKS_BLACK_LIST_ENV is not None:
    links_black_list.extend(LINKS_BLACK_LIST_ENV.split("|"))

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
0.2.8 - Теперь бот сообщает, что завершил работу (только локальная версия!)
0.3 - Добавил возможность добавлять каналы пользователя, чтобы в будущем редактировать/модерировать их. Вести статистику и т.д.
Обновил help, добавил help с перечнем всех возможных команд
Добавил возможность отображать уже добавленные каналы
Обновил получение айдишек стикеров. Теперь лишние ответы будут удалены через 5 секунд.
Добавил обновление данных версий BE для книги через бота. Данные будут взяты из вики и загружены на хостинг
0.3.1 - Добавил обновление баннеров через бота. Данные будут взяты из FB и загружены на хостинг
Обновил существующие функции менюшками, где можно отменить операции, подтвердить и т.д.
Обновил отобржаение HOF и актуальных версий minecraft
Изменил способ подтверждения статуса админов бота (не админов чатов, где есть бот, а именно тех, кто имеет полный доступ к боту)
0.3.1.1 - Добавил хардом ресурсы для сокращения ссылок (+ несколько новых в блок), т.к. нафиг их. Будем банить все совпадения :D
0.3.2 - Сделал первые шаги в создании настроек бота для чатов. Отключение кнопками, удаление старых сообщений (работает как-то криво!) и 
кеширование данных с гита, чтобы уменьшить время ожидания при частых запросах. 

TODO:
Сейчас бот при блокировке ссылки из ЧС оповещает меня в ЛЮБОМ случае. Это плохо, надо перенести этот функционал на админов конкретного чата
Кеширование файлов!
"""
