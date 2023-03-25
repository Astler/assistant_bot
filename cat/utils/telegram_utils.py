import requests
from aiogram import types

from data.config import BOT_TOKEN, MY_PROFILE_ID


def get_message_text(message: types.Message) -> str:
    if message.text is None:
        text = message.caption
    else:
        text = message.text

    return text

def send_telegram_msg_to_me(text: str):
    token = BOT_TOKEN
    chat_id = MY_PROFILE_ID
    url_req = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={text}"
    results = requests.get(url_req)
    print(results.json())