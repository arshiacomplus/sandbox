import os
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database.crud import get_user
from core.ytdlp_engine import download_media
from core.downloader import download_direct
from core.bunkr_engine import is_bunkr_url, download_bunkr
from core.progress import ProgressUpdater
from core.archiver import process_archive
from github_integration.git_manager import push_to_github
from config import YOUTUBE_COOKIES

router = Router()
class DownloadWorkflow(StatesGroup):
    waiting_for_password = State()

@router.callback_query(F.data.startswith("qual_"))
async def process_quality(callback: CallbackQuery, state: FSMContext):
    quality = callback.data.split("_")[1]
    await state.update_data(quality=quality)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="📄 Raw (No Zip)", callback_data="comp_raw")],[InlineKeyboardButton(text="📦 Zip (Max Compression)", callback_data="comp_zip")],[InlineKeyboardButton(text="🔐 Zip with Password", callback_data="comp_pass")]
    ])
    await callback.message.edit_text("⚙️ **Quality selected!**\nHow should I process this?", reply_markup=keyboard, parse_mode="Markdown")

@router.callback_query(F.data.startswith("comp_"))
async def process_compression(callback: CallbackQuery, state: FSMContext):
    comp_type = callback.data.split("_")[1]
    if comp_type == "pass":
        await callback.message.edit_text("🔐 **Send password for the Zip file:**", parse_mode="Markdown")
        await state.set_state(DownloadWorkflow.waiting_for_password)
        return
    await state.update_data(compression=comp_type)
    status_msg = await callback.message.edit_text("⏳ **Initializing...**", parse_mode="Markdown")
    await prepare_download_task(status_msg, state)

@router.message(DownloadWorkflow.waiting_for_password)
async def handle_password(message: Message, state: FSMContext):
    password = message.text.strip()
    await state.update_data(compression="zip_pass", zip_password=password)
    await state.set_state(None)
    status_msg = await message.answer("⏳ **Initializing...**", parse_mode="Markdown")
    await prepare_download_task(status_msg, state)

async def prepare_download_task(message: Message, state: FSMContext):
    data = await state.get_data()
    url = data.get("target_url")
    quality = data.get("quality")
    comp_mode = data.get("compression")
    password = data.get("zip_password", "None")
    is_local = data.get("is_local_file", False)
    await state.clear()

    user = get_user(message.chat.id)
    await message.edit_text("🔄 **Starting Engine...**", parse_mode="Markdown")
    updater = ProgressUpdater(message, action_text="Processing")

    try:
        downloaded_file = None
        if is_local:
            downloaded_file = url
        else:
            updater.action_text = "Downloading File"
            media_domains =["youtube.com", "youtu.be", "twitch.tv", "reddit.com", "vimeo.com", "soundcloud.com"]

            if is_bunkr_url(url):
                downloaded_file = await download_bunkr(url, updater)
            elif any(domain in url for domain in media_domains):
                downloaded_file = await download_media(url, quality, updater, YOUTUBE_COOKIES)
            else:
                downloaded_file = await download_direct(url, updater)

        if not downloaded_file or not os.path.exists(downloaded_file):
            await message.edit_text("❌ **Failed to retrieve file.**", parse_mode="Markdown")
            return

        final_files = await process_archive(downloaded_file, comp_mode, password, updater)
        raw_links = await push_to_github(message.chat.id, user, final_files, updater)

        for f in final_files:
            if os.path.exists(f): os.remove(f)

        links_text = "\n\n".join(raw_links)
        await message.edit_text(f"✅ **Completed!**\n\n{links_text}", parse_mode="Markdown", disable_web_page_preview=True)

    except Exception as e:
        await message.edit_text(f"❌ **Failed:**\n`{str(e)}`", parse_mode="Markdown")