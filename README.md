<div align="center">
  <h1>🚀 RGit Uploader Bot</h1>
  <p>A powerful Telegram bot that acts as an ultimate download and bypass tool. It downloads direct links, videos, local Telegram files, processes them, and pushes them directly to your GitHub repository to generate filter-free raw direct links.</p>
</div>

---

## ✨ Features

- ⚡ **Blazing Fast Downloads:** Uses `Aria2c` (up to 4 concurrent connections) for direct links.
- 🎬 **Media Extraction:** Integrated with `yt-dlp` to download videos from YouTube, Twitch, Vimeo, Reddit, SoundCloud, and more.
- 🔓 **Bunkr Bypass:** Built-in custom API decryptor to download directly from Bunkr domains without restrictions.
- 📁 **Telegram File Support:** Forward or upload any local file (Document, Video, Audio, Photo) directly to the bot. **Supports large files up to 2GB via Pyrogram!**
- 🗜️ **Smart Archiving & Splitting:** Automatically uses `7-Zip` to compress files. Files larger than `90MB` are split into `.zip.001`, `.zip.002` parts to bypass GitHub's file size limit. Password protection is supported.
- 📝 **Auto `Links.md` Generator:** Automatically updates a `Links.md` file in your repository with categorized download links and timestamps.
- 📊 **Live Progress Bar:** Clean and non-spammy progress updates inside Telegram.
- 🔁 **Smart Cookie Fallback:** Automatically retries downloads without cookies if cookie-based download fails.

---

## 🛠️ Prerequisites

Ensure you have **Python 3.9+** and the required CLI tools installed:

```bash
sudo apt-get update
sudo apt-get install -y aria2 ffmpeg p7zip-full git unzip
```

Install `yt-dlp` (latest binary — recommended over apt version):
```bash
sudo curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp
sudo chmod a+rx /usr/local/bin/yt-dlp
```

> ⚠️ **Important:** Do NOT use `apt install yt-dlp` — the apt version is outdated and will fail on modern YouTube.

---

## ⚙️ Setup & Installation

### Option 1: Using Git (Recommended)
```bash
git clone https://github.com/YOUR_USERNAME/sandbox.git
cd sandbox
```

### Option 2: Using Wget
```bash
wget https://github.com/YOUR_USERNAME/sandbox/archive/refs/heads/main.zip -O sandbox.zip
unzip sandbox.zip
cd sandbox-main
```

**1. Create the Virtual Environment:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**2. Install Python Dependencies:**
```bash
pip install -r requirements.txt
```

**3. Configure Environment Variables:**

Create a `.env` file in the root directory:

```env
# Get this from @BotFather on Telegram
BOT_TOKEN=123456789:YOUR_BOT_TOKEN_HERE

# Database URI (SQLite is default, no setup needed)
DB_URL=sqlite:///database/bot.db

# Telegram API Credentials (REQUIRED for downloading files > 20MB)
# Get these from https://my.telegram.org
TG_API_ID=1234567
TG_API_HASH=your_api_hash_here

# YouTube Cookies — Optional (see cookie setup section below)
# Option A: Path to a cookies.txt file on your server
YOUTUBE_COOKIES=youtube_cookies.txt

# Option B: Paste the entire cookie content in double quotes
# YOUTUBE_COOKIES="# Netscape HTTP Cookie File
# .youtube.com   TRUE   /   TRUE   ..."
```

---

## 🚀 Running the Bot

```bash
python bot.py
```

Or with PM2 for production:
```bash
pm2 start bot.py --name "rgit-bot" --interpreter python3
pm2 save
```

---

## 🤖 Telegram Commands

| Command | Description |
|---|---|
| `/start` | Initialize the bot |
| `/set_token <PAT>` | Link your GitHub Personal Access Token *(requires `Contents: Write` permission)* |
| `/set_repo <username/repo>` | Set your target GitHub repository |
| `/status` | Check your current configuration |

> 💡 Just send any **URL** or **Telegram File** to the bot, choose your quality/compression via inline buttons, and get your raw direct links!

---

## 📱 Setting Up Telegram API (For Large Files > 20MB)

Telegram's standard Bot API restricts file downloads to **20MB**. To bypass this and download files up to **2GB**, you must provide your Telegram API credentials.

1. Log in to [my.telegram.org](https://my.telegram.org).
2. Go to **API development tools**.
3. Create a new application (if you haven't already).
4. Copy your **App api_id** and **App api_hash**.
5. Add them to your `.env` file under `TG_API_ID` and `TG_API_HASH`.

---

## 🍪 Setting Up YouTube Cookies (Optional but Recommended)

YouTube may block downloads from server IPs. Providing cookies from a logged-in browser session can help bypass this.

> ⚠️ **Use a secondary/burner Google account** — never your main account.

**Step 1 — Install the browser extension:**
-[Chrome — Get cookies.txt LOCALLY](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)
-[Firefox — Get cookies.txt LOCALLY](https://addons.mozilla.org/en-US/firefox/addon/get-cookies-txt-locally/)

**Step 2 — Export cookies:**
Log in to YouTube, click the extension, and export as `cookies.txt`.

**Step 3 — Add to your server:**
Upload `cookies.txt` to your bot's directory, then in `.env`:
```env
YOUTUBE_COOKIES=youtube_cookies.txt
```

**Step 4 — Restart the bot.**

> 💡 **Note:** The bot automatically retries without cookies if cookie-based download fails, so it works even if your cookies expire.

---

## 📦 How to Extract Split Zip Files (.zip.001, .zip.002)

Since GitHub limits file sizes to 100MB, the bot splits large files into multiple parts (`.zip.001`, `.zip.002`, etc.). Here is how to easily extract them:

### 📱 On Android (Termux)
1. Install `p7zip`:
   ```bash
   pkg update
   pkg install p7zip
   ```
2. Navigate to your download folder and extract the **first part** (it will automatically find and merge the rest of the parts):
   ```bash
   7z x your_file_name.zip.001
   ```

### 💻 On Windows / PC
1. Download all parts (`.001`, `.002`, etc.) and put them in the **same folder**.
2. Install [7-Zip](https://www.7-zip.org/) or [WinRAR](https://www.win-rar.com/).
3. Right-click on the **`.zip.001`** file and select **Extract Here**.

---

## 📁 Project Structure

```
.
├── bot.py                    # Entry point
├── config.py                 # Environment config
├── requirements.txt
├── .env                      # Your secrets (never commit this!)
├── core/
│   ├── archiver.py           # 7zip compression & splitting
│   ├── bunkr_engine.py       # Bunkr API bypass downloader
│   ├── downloader.py         # Aria2c direct downloader
│   ├── progress.py           # Telegram progress bar
│   ├── tg_downloader.py      # Pyrogram engine for large files
│   └── ytdlp_engine.py       # yt-dlp media downloader
├── database/
│   ├── models.py             # SQLAlchemy models
│   └── crud.py               # DB operations
├── github_integration/
│   └── git_manager.py        # Git clone/push logic
└── handlers/
    ├── commands.py           # Bot commands
    ├── messages.py           # URL & file handlers
    └── callbacks.py          # Inline keyboard callbacks
```

---

## 🔑 GitHub PAT Setup

1. Go to **GitHub → Settings → Developer Settings → Personal Access Tokens → Tokens (classic)**
2. Click **Generate new token (classic)**
3. Give it a name, set expiration, and check **`repo` → `Contents: Write`**
4. Copy the token and send `/set_token <your_token>` to the bot

---

## ⚠️ Important Notes

- GitHub has a **100MB hard limit** per file. The bot automatically splits files at **90MB** to stay safe.
- The `Links.md` file in your repo is updated automatically with every upload and includes Tehran (IR) timestamps.
- `tmp_downloads/` is used as a working directory and is cleaned up after each upload.
- Do **not** commit your `.env` file or `youtube_cookies.txt` — add them to `.gitignore`.

```gitignore
.env
youtube_cookies.txt
tmp_downloads/
database/bot.db
```

---

<div align="center">
  <p>Made with ❤️ — Pull requests welcome!</p>
</div>