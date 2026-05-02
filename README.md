<div align="center">
  <h1>🚀 RGit Uploader Bot (v2.0)</h1>
  <p>A powerful Telegram bot that acts as an ultimate download and bypass tool. It downloads direct links, videos, local Telegram files, processes them, and pushes them directly to your GitHub repository to generate filter-free raw direct links.</p>
</div>

---

## ✨ Features
- ⚡ **Blazing Fast Downloads:** Uses `Aria2c` (up to 4 concurrent connections) for direct links.
- 🎬 **Media Extraction:** Integrated with `yt-dlp` to download videos from YouTube, Twitch, Vimeo, Reddit, SoundCloud, and more.
- 🔓 **Bunkr Bypass:** Built-in custom API decryptor to download directly from Bunkr domains without restrictions.
- 📁 **Telegram File Support:** You can forward or upload any local file (Document, Video, Audio, Photo) directly to the bot, and it will upload it to GitHub.
- 🗜️ **Smart Archiving & Splitting:** Automatically uses `7-Zip` to compress files. If a file is larger than `95MB`, it smartly splits it into `.zip.001`, `.zip.002` parts to bypass GitHub's strict file size limit. Password protection is supported.
- 📝 **Auto `Links.md` Generator:** Automatically updates a `Links.md` file in your repository with categorized download links and timestamps for easy access.
- 📊 **Live Progress Bar:** Clean and non-spammy progress updates inside Telegram.

## 🛠️ Prerequisites
Before running the bot, ensure you have Python 3.9+ and the required CLI tools installed on your Linux machine or server:

```bash
sudo apt-get update
sudo apt-get install -y aria2 ffmpeg p7zip-full git unzip
```

## ⚙️ Setup & Installation

You can download the bot using either **Git** or **Wget**.

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

---

**1. Create the Virtual Environment:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**2. Install Python Dependencies:**
```bash
pip install -r requirements.txt
```

**3. Environment Variables (.env):**
Create a `.env` file in the root directory and add your bot credentials:
```env
# Get this from @BotFather in Telegram
BOT_TOKEN=123456789:YOUR_BOT_TOKEN_HERE

# Database URI (SQLite is default)
DB_URL=sqlite:///database/bot.db

# YouTube Cookies (Optional but Recommended)
# Paste the ENTIRE content of your cookies.txt file INSIDE double quotes
YOUTUBE_COOKIES="paste_your_cookies_here"
```

## 🚀 Running the Bot
Once everything is set up, run the bot using:
```bash
python bot.py
```

## 🤖 Usage (Telegram Commands)
Open your bot in Telegram and use the following commands to get started:
- `/start` - Initialize the bot.
- `/set_token <PAT>` - Securely link your GitHub Personal Access Token. *(Requires `Contents: Write` permission).*
- `/set_repo <username/repo>` - Set the target repository for uploading.
- `/status` - Check your configuration status.

> 💡 **Tip:** Just send any **URL** or **Telegram File** to the bot, choose your quality/compression settings via Inline Keyboards, and receive your direct raw links!

<hr/>

## 🍪 Setting Up YouTube Cookies (Optional but Recommended)
YouTube often blocks automated downloads. To bypass this, you can provide global cookies for your bot:

1. **Install Browser Extension:** Install the `Get cookies.txt LOCALLY` extension on your PC browser:
   - [🌐 Chrome Web Store](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)
   - [🌐 Firefox Add-ons](https://addons.mozilla.org/en-US/firefox/addon/get-cookies-txt-locally/)
2. **Export Cookies:** Log in to YouTube (preferably with a secondary/burner account), click the extension icon, and select **Export As**. Save the `cookies.txt` file to your PC.
3. **Add to `.env`:** Open your `.env` file and add the `YOUTUBE_COOKIES` variable. Paste the entire content of the file **inside double quotes (`""`)**.

Example:
```env
BOT_TOKEN=123456789:YOUR_BOT_TOKEN_HERE
DB_URL=sqlite:///database/bot.db

YOUTUBE_COOKIES="# Netscape HTTP Cookie File
.youtube.com    TRUE    /    TRUE    1745423871    LOGIN_INFO    ...
(paste the rest of your cookie content here)"
```
4. **Restart the bot.** Now the bot will securely use this global cookie for all YouTube downloads!
