from aiogram import types
from aiogram.dispatcher.filters import AdminFilter

from loader import dp, bot
from utils.group_data.data import get_group_dict, save_group_dict


@dp.message_handler(AdminFilter(), commands=["edit_hero_name", "set_hero_name"])
async def hero_of_the_day(message: types.Message):
    new_name = message.get_args()

    if len(new_name) == 0:
        await bot.send_message(message.chat.id, "Так не сработает. Введите имя сразу после команды в формате: "
                                                "/set_hero_name Новое имя")
        return

    chat_id = message.chat.id

    group_info = get_group_dict(chat_id)

    if message.chat.title == new_name:
        await bot.send_message(message.chat.id, "Ничего не изменилось")
    else:
        group_info.hero_name = new_name
        await bot.send_message(message.chat.id, f"Меняю имя для \"Героя дня\" на \"{new_name}\"")

    save_group_dict(chat_id, group_info)
