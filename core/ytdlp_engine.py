import os
import asyncio
import uuid
import re
import glob
from core.progress import ProgressUpdater

async def download_media(url: str, quality: str, updater: ProgressUpdater, user_cookies: str = None):
    tmp_dir = "tmp_downloads"
    os.makedirs(tmp_dir, exist_ok=True)

    cmd = ["yt-dlp", "--newline", "--no-warnings"]

    cookies_file_to_delete = None
    if user_cookies:
        if os.path.isfile(user_cookies):
            cmd.extend(["--cookies", user_cookies])
        elif len(user_cookies.strip()) > 20:
            cookies_file_to_delete = os.path.join(tmp_dir, f"cookies_{uuid.uuid4().hex[:6]}.txt")
            with open(cookies_file_to_delete, "w", encoding="utf-8") as f:
                f.write(user_cookies.strip())
            cmd.extend(["--cookies", cookies_file_to_delete])

    if quality == "720p":
        ytdlp_args = ["-f", "bestvideo[height<=720]+bestaudio/best[height<=720]/best", "--merge-output-format", "mp4"]
    elif quality == "480p":
        ytdlp_args = ["-f", "bestvideo[height<=480]+bestaudio/best[height<=480]/best", "--merge-output-format", "mp4"]
    elif quality == "360p":
        ytdlp_args = ["-f", "bestvideo[height<=360]+bestaudio/best[height<=360]/best", "--merge-output-format", "mp4"]
    elif quality == "audio":
        ytdlp_args = ["-x", "--audio-format", "mp3"]
    else:
        ytdlp_args = ["-f", "bestvideo+bestaudio/best", "--merge-output-format", "mp4"]
    file_id = uuid.uuid4().hex[:8]
    outtmpl = os.path.join(tmp_dir, f"{file_id}_%(title)s.%(ext)s")

    cmd.extend(ytdlp_args)
    cmd.extend(["-o", outtmpl, url])

    updater.action_text = "Downloading Media"


    import logging
    logging.info(f"[yt-dlp CMD]: {' '.join(cmd)}")

    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT
    )

    regex_progress = re.compile(r'\[download\]\s+([0-9\.]+)%.*at\s+([0-9a-zA-Z\./]+)\s+ETA\s+([0-9:]+)')

    all_output = []

    while True:
        line = await process.stdout.readline()
        if not line:
            break

        text = line.decode('utf-8', errors='ignore').strip()
        all_output.append(text)
        logging.info(f"[yt-dlp]: {text}")

        match = regex_progress.search(text)
        if match:
            try:
                percent = float(match.group(1))
                speed = match.group(2)
                eta = match.group(3)
                updater.update_sync(percent, speed, eta)
            except:
                pass

    await process.wait()

    if cookies_file_to_delete and os.path.exists(cookies_file_to_delete):
        os.remove(cookies_file_to_delete)

    downloaded_files = glob.glob(os.path.join(tmp_dir, f"{file_id}_*"))
    if downloaded_files:
        return downloaded_files[0]
    else:

        error_text = "\n".join(all_output[-10:])
        raise Exception(f"yt-dlp failed:\n{error_text}")