import io

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, AdminFilter
from aiogram.dispatcher.filters.state import StatesGroup, State

from filters import IsGroup
from loader import dp, bot


class PhotoState(StatesGroup):
    photoWait = State()


@dp.message_handler(IsGroup(), Command("set_photo", prefixes="!/"), AdminFilter())
async def set_chat_photo(message: types.Message):
    source_message = message.reply_to_message

    if source_message is None:
        await bot.send_message(message.chat.id,
                               "Отправляйте фото")
        await PhotoState.photoWait.set()

    photo = None

    try:
        photo = source_message.photo[-1]
    except:
        document = source_message.document

        if document is not None:
            photo = await bot.get_file(source_message.document.file_id)

    if photo is not None:
        photo = await photo.download(destination=io.BytesIO())
        input_files = types.InputFile(path_or_bytesio=photo)
        await bot.set_chat_photo(chat_id=message.chat.id, photo=input_files)
        await bot.send_message(message.chat.id, "Фото обновлено!")
    else:
        await bot.send_message(message.chat.id, "Фото не найдено!")


@dp.message_handler(state=PhotoState.photoWait, content_types=types.ContentTypes.PHOTO)
async def get_new_photo_photo(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, "Советую отправлять изображения без сжатия!")
    photo = message.photo[-1]
    photo = await photo.download(destination=io.BytesIO())
    input_files = types.InputFile(path_or_bytesio=photo)
    await bot.set_chat_photo(chat_id=message.chat.id, photo=input_files)
    await bot.send_message(message.chat.id, "Фото обновлено!")
    await state.finish()


@dp.message_handler(state=PhotoState.photoWait, content_types=types.ContentTypes.DOCUMENT)
async def get_new_photo_photo(message: types.Message, state: FSMContext):
    photo = await bot.get_file(message.document.file_id)
    photo = await photo.download(destination=io.BytesIO())
    input_files = types.InputFile(path_or_bytesio=photo)

    try:
        await bot.set_chat_photo(chat_id=message.chat.id, photo=input_files)
        await bot.send_message(message.chat.id, "Фото обновлено!")
    except:
        await bot.send_message(message.chat.id, "При попытке загрузки изображения произошла ошибка. Изображение ли это?")

    await state.finish()


@dp.message_handler(state=PhotoState.photoWait, content_types=types.ContentTypes.ANY)
async def get_new_photo_photo(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, "Это не фото!")
    await state.finish()


@dp.message_handler(IsGroup(), Command("set_title", prefixes="!/"), AdminFilter())
async def set_chat_title(message: types.Message):
    new_name = message.get_args()

    if len(new_name) == 0:
        await bot.send_message(message.chat.id, "Так не сработает. Введите имя сразу после команды в формате: "
                                                "/set_title Новое имя")
    else:
        if message.chat.title == new_name:
            await bot.send_message(message.chat.id, "Вы ввели текущее имя чата!")
        else:
            await bot.set_chat_title(chat_id=message.chat.id, title=new_name)
            await bot.send_message(message.chat.id, f"Меняю имя группы на \"{new_name}\"")


@dp.message_handler(IsGroup(), Command("set_description", prefixes="!/"), AdminFilter())
async def set_chat_description(message: types.Message):
    new_description = message.get_args()

    if len(new_description) == 0:
        await bot.send_message(message.chat.id, "Так не сработает. Введите новое описание сразу после команды в "
                                                "формате: /set_description Описание")
    else:
        chat = await bot.get_chat(chat_id=message.chat.id)
        if chat.description == new_description:
            await bot.send_message(message.chat.id, "Вы ввели текущее описание чата!")
        else:
            await bot.set_chat_description(chat_id=message.chat.id, description=new_description)
            await bot.send_message(message.chat.id, f"Меняю описание группы на \"{new_description}\"")
