from aiogram import types
from aiogram.dispatcher.filters import CommandHelp

from bot.filters import IsPrivate, BotSuperAdminsFilter
from loader import dp
from utils.misc import rate_limit


@rate_limit()
@dp.message_handler(CommandHelp(), IsPrivate(), BotSuperAdminsFilter())
async def bot_help(message: types.Message):
    text = [
        'Технические',
        '/id - бот вернет ваш id в TG (только в ЛС!)\n'
        '/sticker_id - бот вернет айди всех отправленных стикеров (только в ЛС!)',
        '/add_channel - добавить свой канал для публикации постов/редактирования (только в ЛС!)(в разработке!)',
        '/my_channels - список ваших каналов (только в ЛС!)(уже можно добавить канал, но смысл?)',
        '/profile - настройки поведения бота и заданные параметры (только в ЛС!)(в разработке!)',
        '/profile true/false - включение/отключение очистки команд (только в ЛС!)',
        '/chat_id - отображает id чата, но может быть вызвана только админом (только в группах!)'
        '/set_photo - меняет фото чата. Можно использовать как reply сообщения, так и отправить после ввода '
        'команды. Поддерживает как сжатые фото, так и отправленные в виде документа (только в группах!)',
        '/set_title NEW_NAME - меняет название чата. Новое имя пишем вместо NEW_NAME (только в группах!)',
        '/set_description NEW_DESCRIPTION - меняет описание чата. Новое описание пишем вместо '
        'NEW_DESCRIPTION (только в группах!)',
        '/add_black_link LINK - добавляет ссылку в чёрный список ЭТОГО чата. Работает, но никак не реагирует'
        ' (в разработке!)(только в группах!)',
        '/ro REASON TIME - вызываем в ответ на сообщение того, кому хотим дать мут. Первый параметр причина, '
        'второй - время в минутах (только в группах!)',
        '',
        'Дополнительные',
        '/hof - отображает список HOF (только в группах!)',
        '/minecraft_versions - отображает актуальные версии JE и BE изданий игры (только в группах!)',
        '',
        'Функции *superadmin* уровня доступа!',
        '/update_be_versions - обновить версии BE для KB App (только в ЛС!)',
        '/update_hof_versions - внести правки в HOF (только в ЛС!)',
        '/update_banners_search_map - обновить мапу для поиска баннеров для BE (только в ЛС!)',
    ]

    formatted_text = '\n'.join(text)

    await message.answer(formatted_text)
