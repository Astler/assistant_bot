from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from github import Github

from data import config
from data.config import GITHUB_TOKEN, GITHUB_REPO

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

github = Github(GITHUB_TOKEN)
repository = github.get_user().get_repo(GITHUB_REPO)
