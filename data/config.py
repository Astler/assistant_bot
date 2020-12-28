
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str("1280483802:AAHNu0JihLQBIZlP1qBsK3pasuNTeFeG7Ns")

admins = [
    376225089
]

ip = "localhost"

aiogram_redis = {
    'host': ip,
}

redis = {
    'address': (ip, 6379),
    'encoding': 'utf8'
}
