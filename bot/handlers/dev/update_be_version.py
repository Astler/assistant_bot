from aiogram import types
from aiogram.dispatcher import FSMContext

from filters import IsPrivate, BotAdminsFilter
from loader import dp
from utils.minecraft.be_version_updater import be_version_get, be_version_push
from utils.misc import rate_limit


@rate_limit()
@dp.message_handler(IsPrivate(), BotAdminsFilter(), commands="update_be_versions")
async def manual_update(message: types.Message, state: FSMContext):
    updating_message = await message.reply("Updating...")
    await be_version_push(await be_version_get())
    await updating_message.delete()