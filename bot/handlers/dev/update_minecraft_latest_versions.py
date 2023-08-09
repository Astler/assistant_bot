from aiogram import types

from bot.filters import IsPrivate, BotSuperAdminsFilter
from loader import dp
from utils.minecraft.minecraft_version_updater import minecraft_versions_get, minecraft_version_push
from utils.misc import rate_limit


@rate_limit()
@dp.message_handler(IsPrivate(), BotSuperAdminsFilter(), commands="update_be_versions")
async def manual_update(message: types.Message):
    updating_message = await message.reply("Updating...")
    await minecraft_version_push(await minecraft_versions_get())
    await updating_message.delete()
