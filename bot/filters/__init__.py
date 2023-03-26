from aiogram import Dispatcher

from bot.filters.cat_admin_filter import BotSuperAdminsFilter
from bot.filters.forward_from_reply import ForwardFromReply
from bot.filters.is_group import IsGroup
from bot.filters.is_only_dots_in_msg import IsDotsMessage
from bot.filters.private_chat import IsPrivate
from bot.filters.random_item_filter import RandomItemFilter
from bot.filters.reputation_filter import ReputationFilter
from bot.filters.who_is_today_filter import ChooseItemFilter


def setup(dp: Dispatcher):
    pass
    dp.filters_factory.bind(BotSuperAdminsFilter)
    dp.filters_factory.bind(ForwardFromReply)
    dp.filters_factory.bind(IsGroup)
    dp.filters_factory.bind(IsDotsMessage)
    dp.filters_factory.bind(IsPrivate)
    dp.filters_factory.bind(RandomItemFilter)
    dp.filters_factory.bind(ReputationFilter)
    dp.filters_factory.bind(ChooseItemFilter)
