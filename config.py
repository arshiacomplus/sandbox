import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_URL = os.getenv("DB_URL", "sqlite:///database/bot.db")
YOUTUBE_COOKIES = os.getenv("YOUTUBE_COOKIES", "")

if not BOT_TOKEN:
    raise ValueError("⚠️ BOT_TOKEN is not set in .env file!")