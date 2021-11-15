from aiogram.utils.callback_data import CallbackData

cancel_action_callback = CallbackData("cancel", "action")
simple_callback = CallbackData("callback", "action")

post_creation_callback = CallbackData("post", "action")

bot_group_settings = CallbackData("bot_group_settings", "action")
