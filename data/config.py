import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TOKEN_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

MY_PROFILE_ID = os.getenv("MY_PROFILE_ID")

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN_KEY")
INSTANCE_UNIQUE_NAME = os.getenv("INSTANCE_UNIQUE_NAME")
HOF_URL = os.getenv("HOF_URL")
GITHUB_REPO = os.getenv("GITHUB_REPO")
A_PATH = os.getenv('A_PATH')

FTP_URL = os.getenv('FTP_URL')
FTP_USER = os.getenv('FTP_USER')
FTP_PASS = os.getenv('FTP_PASS')

HOF_FILE = os.getenv('HOF_FILE')

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

if not str(os.getenv('PORT')).__contains__("None"):
    WEBAPP_PORT = os.getenv('PORT', default=8000)

CHATS_ENV = os.getenv("CHATS").split("|")

BOT_NAMES = os.getenv('BOT_NAMES').split("|")




chats = [int(admin) for admin in CHATS_ENV]

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

version = "0.4.7.3"

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
0.3.2.1 - фикс записи?
0.3.3 - +rep -rep сырая реализация
0.3.3.1 - фиксы репутации
0.3.3.2 - фиксы вылета репутации у юзеров без никнейма
0.3.3.3 - добавил задержку изменения репутации, изменил аккаунт деплоя, т.к. старый потерял ((
0.3.3.4 - пофиксил баги, почистил код, добавил my_rep комманду, которая покажет репутацию юзера конкретно в этом чате!
0.3.4 - добавил команду all_in_chat, которая отвечает списком всех пользователей в чате
0.3.5 - на базе предыдущей команды добавил фичу ПДР дня, а также режим злого бота, в котором она доступна
Напротив, если режим не злой, то не в статах этих данных не будет, ни сама функция работать не будет
0.3.5.1 - фиксить пытаюсь баг с перезаписью данных
0.3.5.2 - рейтинг пользователей группы
0.3.5.3 - фикс пустых локальных кешированных данных
0.3.6 - добавлена реакция на сообщения из точек
0.3.6.1 - фикс реакции
0.3.7 - запрос ИЛИ
0.3.7.1 - pidor_stats - отображает всех героев по дням
0.3.8 - help updated for groups and rep triggers updated
0.3.8.1 - fixed group help
0.3.8.2 - fixed trottler
0.3.8.3 - cowsay
0.3.8.4 - cowsay fix
0.3.8.5 - cowsay hero choose
0.3.8.5 - cowsay hero choose fix
0.3.9 - fixed group data use in code. Added custom "hero of the day", redone pidor_stats
0.3.9.1 - fixes
0.3.9.2 - group data fixes
0.3.9.3 - hero command fix
0.3.9.4 - updated BE version check logic
0.4 - Friendly Update!
Updated minecraft_versions and choose_random_item features to work in private and fixes bugs with them. Also added common handlers dit for commands
Added /all_members variation: "all_abroad"
Deleted echo command
Deleted dots smile
Updated ban, added rep system keys
0.4.1 - Spring Clean (at July)
Updated "Only private" response
Updated users data
0.4.1.1 - Fixes
Fixed "hero of day" command
Fixed no lowercase cast in rep keywords
0.4.2 - Bye heroku!
0.4.3 - added passgen command. Just to create random passwords, idk
0.4.3.1 - passgen fix
0.4.3.2 - base /passgen finished
0.4.4 - fixed minecraft wiki parser
0.4.4.1 - started listener rework
0.4.4.2 - listener WIP2, updated libs
0.4.5 - updated project hierarchy, updated dev commands, finished test version of channels listener
0.4.5.1 - fixed missed requirements
0.4.5.2 - docker input fix
0.4.5.3 - docker input fix #2
0.4.5.4 - listener fixes, moved to pyrogram
0.4.6 - open ai playground and listener improvements
0.4.6.1 - clean up
0.4.6.2 - updated model code, added logic to add and check data
0.4.7 - removed learning model logic, updated filters
0.4.7.1 - fixes
0.4.7.2 - git push fixes
0.4.7.3 - listener fixes (mb)

TODO:
Global user data
Channel manage
Better url block system
Rework user settings
"""
