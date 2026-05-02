import os
import uuid
from pyrogram import Client
from core.progress import ProgressUpdater

async def download_large_tg_file(
    api_id: int,
    api_hash: str,
    bot_token: str,
    message_id: int,
    chat_id: int,
    ext: str,
    updater: ProgressUpdater
) -> str:
    tmp_dir = "tmp_downloads"
    os.makedirs(tmp_dir, exist_ok=True)
    local_name = f"tg_{uuid.uuid4().hex[:6]}{ext}"
    file_path = os.path.join(tmp_dir, local_name)

    async with Client(
        name="rgit_bot_session",
        api_id=api_id,
        api_hash=api_hash,
        bot_token=bot_token,
        in_memory=True
    ) as app:
        msg = await app.get_messages(chat_id, message_id)

        def progress(current, total):
            if total:
                percent = (current / total) * 100
                updater.update_sync(percent, f"{current//1024//1024}MB", "Calc...")

        await app.download_media(msg, file_name=file_path, progress=progress)

    return file_path