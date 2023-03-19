import requests

from data.config import BOT_TOKEN, MY_PROFILE_ID


def send_telegram_msg_to_me(text: str):
    token = BOT_TOKEN
    chat_id = MY_PROFILE_ID
    url_req = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={text}"
    results = requests.get(url_req)
    print(results.json())