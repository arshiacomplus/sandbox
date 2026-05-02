import os
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from database.crud import create_or_update_user, get_user
from config import YOUTUBE_COOKIES

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    create_or_update_user(message.from_user.id)
    welcome_text = (
        "👋 **Welcome to RGit uploader!**\n\n"
        "I'm here to bypass restrictions and upload files directly to your GitHub repository.\n\n"
        "⚙️ **Setup Instructions:**\n"
        "1️⃣ `/set_token <YOUR_GITHUB_PAT>` - Set your PAT.\n"
        "2️⃣ `/set_repo <username/repo>` - Set your target repository.\n\n"
        "💡 *Just send me any direct link, file, or media URL to start!*"
    )
    await message.answer(welcome_text, parse_mode="Markdown")

@router.message(Command("set_token"))
async def set_token(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("⚠️ **Usage:** `/set_token <PAT>`", parse_mode="Markdown")
        return
    create_or_update_user(message.from_user.id, github_token=args[1].strip())
    await message.answer("✅ **GitHub Token saved!**", parse_mode="Markdown")

@router.message(Command("set_repo"))
async def set_repo(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("⚠️ **Usage:** `/set_repo <user/repo>`", parse_mode="Markdown")
        return
    create_or_update_user(message.from_user.id, github_repo=args[1].strip())
    await message.answer(f"✅ **Repo set to:** `{args[1].strip()}`", parse_mode="Markdown")

@router.message(Command("status"))
async def cmd_status(message: Message):
    user = get_user(message.from_user.id)
    if not user: return

    t_st = "✅" if user.github_token else "❌"
    r_st = f"✅ `{user.github_repo}`" if user.github_repo else "❌"
    c_st = "✅ (Global)" if YOUTUBE_COOKIES else "❌ `Not set in .env`"

    text = f"📊 **Status:**\n\n🔑 **User Token:** {t_st}\n📁 **User Repo:** {r_st}\n🍪 **Global Cookies:** {c_st}"
    await message.answer(text, parse_mode="Markdown")