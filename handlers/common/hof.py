from aiogram import types
from aiogram.types import ParseMode

from bot.filters import BotSuperAdminsFilter, IsPrivate
from loader import dp, bot
from utils.hof.hof_utils import load_hof_array
from utils.misc import rate_limit

@rate_limit()
@dp.message_handler(IsPrivate(), BotSuperAdminsFilter(), commands="hof")
async def bot_start(message: types.Message):
    msg = await bot.send_message(message.chat.id, "Начинаю загрузку данных HOF...")

    result = load_hof_array()

    if not isinstance(result, list):
        await message.reply(result)
        return

    output_msg = [f"*{item.name}*\n{item.description}" for item in result]
    data_from_server = "\n\n".join(output_msg)

    await msg.edit_text(
        f"Спасибо всем, кто помогал и продолжает помогать! Пингуйте если в списке не нашли себя!\n\n{data_from_server}",
        parse_mode=ParseMode.MARKDOWN)
