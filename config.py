import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_URL = os.getenv("DB_URL", "sqlite:///database/bot.db")
YOUTUBE_COOKIES = os.getenv("YOUTUBE_COOKIES", "")
TG_API_ID = int(os.getenv("TG_API_ID", 0))
TG_API_HASH = os.getenv("TG_API_HASH", "")
if not BOT_TOKEN:
    raise ValueError("⚠️ BOT_TOKEN is not set in .env file!")