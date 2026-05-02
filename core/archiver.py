import os
import uuid
import asyncio
import re


def sanitize_filename(name):
    return re.sub(r'[^\w\.\-]', '_', name)


async def split_file(file_path: str, chunk_mb: int, base_name: str, dir_name: str) -> list:
    """فایل بزرگ رو به تیکه‌های کوچیک تقسیم کن"""
    chunk_size = chunk_mb * 1024 * 1024
    parts = []
    part_num = 1

    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            part_path = os.path.join(dir_name, f"{base_name}.zip.{part_num:03d}")
            with open(part_path, 'wb') as pf:
                pf.write(chunk)
            parts.append(part_path)
            part_num += 1

    return parts


async def process_archive(file_path: str, comp_mode: str, password: str, updater):
    updater.action_text = "📦 Processing File"

    file_path = os.path.abspath(file_path)
    dir_name = os.path.dirname(file_path)

    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    raw_base = os.path.splitext(os.path.basename(file_path))[0]
    ext = os.path.splitext(file_path)[1]

    base_name = sanitize_filename(raw_base)
    unique_id = str(uuid.uuid4())[:8]
    new_base = f"{base_name}_{unique_id}"


    if comp_mode == "raw" and file_size_mb <= 95:
        final_path = os.path.join(dir_name, f"{new_base}{ext}")
        os.rename(file_path, final_path)
        return [final_path]

    needs_split = file_size_mb > 95
    has_password = password and password != "None"
    zip_path = os.path.join(dir_name, f"{new_base}.zip")

    if has_password:

        cmd = ["7z", "a", "-tzip", "-mx=9", f"-p{password}", zip_path, file_path]

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await process.communicate()

        if os.path.exists(file_path):
            os.remove(file_path)

        if not os.path.exists(zip_path):
            raise Exception("Archiving with password failed!")


        if needs_split:
            parts = await split_file(zip_path, 95, new_base, dir_name)
            os.remove(zip_path)
            return parts

        return [zip_path]

    else:

        if needs_split:
            cmd = ["zip", "-j", "-9", "-s", "95m", zip_path, file_path]
        else:
            cmd = ["zip", "-j", "-9", zip_path, file_path]

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await process.communicate()

        if os.path.exists(file_path):
            os.remove(file_path)


        all_files = sorted([
            os.path.join(dir_name, f)
            for f in os.listdir(dir_name)
            if f.startswith(new_base) and (
                f.endswith(".zip") or re.match(r'.*\.z\d+$', f)
            )
        ])

        if not all_files:
            raise Exception("Archiving failed! No output files found.")


        if len(all_files) == 1:
            return all_files


        zparts = sorted([f for f in all_files if not f.endswith(".zip")])
        zmain = [f for f in all_files if f.endswith(".zip")]
        return zparts + zmain