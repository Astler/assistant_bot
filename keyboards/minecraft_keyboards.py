from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def minecraft_versions_keyboard(versions_dict: dict):
    keyboard = InlineKeyboardMarkup()

    wiki_url = 'https://minecraft.fandom.com/ru/wiki/'

    dict_size = len(versions_dict)

    can_be_paired = dict_size % 2 == 0

    if can_be_paired:
        keys = list(versions_dict.keys())

        for i in range(0, dict_size, 2):
            keyboard.add(
                InlineKeyboardButton(keys[i], url=wiki_url + versions_dict[keys[i]]),
                InlineKeyboardButton(keys[i + 1], url=wiki_url + versions_dict[keys[i + 1]])
            )
    else:
        for item in versions_dict:
            keyboard.add(InlineKeyboardButton(item, url=wiki_url + versions_dict[item]))

    return keyboard
