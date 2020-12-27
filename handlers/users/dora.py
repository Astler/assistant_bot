import asyncio

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from filters import IsPrivate
from loader import dp


@dp.message_handler(commands="print_fool")
async def bot_welcome_bed(message: types.Message):
    await message.answer("3!")
    await asyncio.sleep(1)
    await message.answer("2!")
    await asyncio.sleep(1)
    await message.answer("1!")
    await asyncio.sleep(1)
    await message.answer("Привет, Даша!")
    await message.answer("3!")
    await asyncio.sleep(1)
    await message.answer("2!")
    await asyncio.sleep(1)
    await message.answer("1!")
    await asyncio.sleep(1)
    await message.answer("Python - это круто!")


@dp.message_handler(commands="print_good")
async def bot_welcome_good(message: types.Message):
    await count_back(message)
    await hello_dora(message)
    await count_back(message)
    await python_is_cool(message)


async def hello_dora(message: types.Message):
    await message.answer("Привет, Даша!")


async def python_is_cool(message: types.Message):
    await message.answer("Python - это круто!")


async def count_back(message: types.Message):
    await message.answer("3!")
    await asyncio.sleep(1)
    await message.answer("2!")
    await asyncio.sleep(1)
    await message.answer("1!")
    await asyncio.sleep(1)


@dp.message_handler(CommandStart(), IsPrivate())
async def bot_start(message: types.Message):
    await message.answer(f'Привет, {message.from_user.full_name}!')


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f'Приветствуем, {message.from_user.full_name} {message.from_user.id}!')
