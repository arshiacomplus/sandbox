import os
import uuid
import asyncio
import re
import logging

def sanitize_filename(name):
    return re.sub(r'[^\w\.\-]', '_', name)

async def process_archive(file_path: str, comp_mode: str, password: str, updater):
    updater.action_text = "📦 Processing File"

    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    raw_base = os.path.splitext(os.path.basename(file_path))[0]
    ext = os.path.splitext(file_path)[1]

    base_name = sanitize_filename(raw_base)
    unique_id = str(uuid.uuid4())[:8]
    new_base = f"{base_name}_{unique_id}"
    dir_name = os.path.dirname(file_path)


    if comp_mode == "raw" and file_size_mb <= 95:
        final_path = os.path.join(dir_name, f"{new_base}{ext}")
        os.rename(file_path, final_path)
        return [final_path]

    needs_split = file_size_mb > 95
    zip_path = os.path.join(dir_name, f"{new_base}.zip")
    cmd = ["7z", "a", "-tzip", "-mx=9"]

    if needs_split:
        cmd.append("-v95m")

    if password and password != "None":
        cmd.append(f"-p{password}")

    cmd.extend([zip_path, file_path])

    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()

    logging.info(f"[archiver] 7z returncode: {process.returncode}")
    logging.info(f"[archiver] 7z stdout: {stdout.decode()}")
    logging.info(f"[archiver] 7z stderr: {stderr.decode()}")
    logging.info(f"[archiver] cmd: {' '.join(cmd)}")
    all_in_dir = os.listdir(dir_name)
    logging.info(f"[archiver] Files in dir: {all_in_dir}")
    logging.info(f"[archiver] Looking for prefix: {new_base}")

    if os.path.exists(file_path):
        os.remove(file_path)


    all_files = sorted([
        os.path.join(dir_name, f)
        for f in os.listdir(dir_name)
        if f.startswith(new_base)
    ])

    if not all_files:
        raise Exception("Archiving failed! No output files found.")


    if len(all_files) == 1:
        single = all_files[0]

        if single.endswith(".001"):
            clean_path = single[:-4]
            os.rename(single, clean_path)
            return [clean_path]
        return [single]


    return all_files