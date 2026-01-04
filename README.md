# lyricsync

A Discord bot that fetches song lyrics using the LRCLIB API and displays the lyrics in paginated embeds.

Supports both slash commands and traditional prefix commands.

---

## Features

- `/lyrics` slash command
- `!lyrics` prefix command
- Automatic pagination for long lyrics (So, basically anything above 1900 words)
- Interactive navigation buttons
- Uses LRCLIB as the lyrics source
- Async and lightweight

---

## Commands

### Slash Command
/lyrics (song name) (artist name)

---

## Setup

### 1. Clone the repository
```
git clone https://github.com/piarsquared/lyricsync
cd lyricsync
```
> [!NOTE]
> This will download the optional ```main.py``` that is in the optional folder. This removes any of the cute things in case you don't like that. Simply swap the main.py files

## Dependencies 
pip install -r requirements.txt

This will download:

- discord.py
- aiohttp
- python-dotenv

> [!NOTE]
> Lyrics are provided by lrclib.net.
> Embed content is limited to Discord's 2000 character limit.
> Buttons timeout after 3 minutes
