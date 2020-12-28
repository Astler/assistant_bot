from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery

from keyboards.inline.base_callback_data import links_callback, back_callback
from keyboards.inline.base_menu import links_menu, author_links, apps_links, other_links
from loader import dp, bot


@dp.message_handler(Command("links"))
async def get_user_links(message: types.Message):
    await message.answer(text="Список доступных ссылок быстрого доступа", reply_markup=links_menu)


@dp.callback_query_handler(links_callback.filter(links_group_name="author"))
async def load_links_by_group(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    await call.message.edit_reply_markup()
    await call.message.answer("Вот ссылки для на мои аккаунты!", reply_markup=author_links)
    await call.message.delete()


@dp.callback_query_handler(links_callback.filter(links_group_name="apps"))
async def load_links_by_group(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    await call.message.edit_reply_markup()
    await call.message.answer("Вот ссылки для на мои приложения!", reply_markup=apps_links)
    await call.message.delete()


@dp.callback_query_handler(links_callback.filter(links_group_name="other"))
async def load_links_by_group(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    await call.message.edit_reply_markup()
    await call.message.answer("Ещё полезные ссылки!", reply_markup=other_links)
    await call.message.delete()


@dp.callback_query_handler(back_callback.filter(back_menu_name="back_to_links_menu"))
async def load_links_by_group(call: CallbackQuery, callback_data: dict):
    await call.message.edit_reply_markup()
    await call.message.answer(text="Вот список доступных ссылок быстрого доступа", reply_markup=links_menu)
    await call.message.delete()


@dp.callback_query_handler(text="cancel")
async def cancel_all(call: CallbackQuery):
    await call.message.answer(text="Меню ссылок закрыто")
    await call.message.delete()
