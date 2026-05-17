# MineBot

A simple Discord bot for a Minecraft community.

## Features

- `!hello` checks that the bot is online.
- `!ping` shows bot latency.
- `!mc` shows Minecraft server details.
- `!rules` shows the server rules.
- `!whitelist <minecraft_name>` receives whitelist requests.
- `!ticket <message>` receives basic support requests.
- `!about` shows bot info.

## Setup

1. Install Python 3.10 or newer.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env`.
4. Put your Discord bot token in `.env`:

```env
DISCORD_TOKEN=your-real-token
MINECRAFT_SERVER_IP=your-server-ip
MINECRAFT_VERSION=1.20+
STAFF_CHANNEL_ID=optional-staff-channel-id
```

5. Run the bot:

```bash
python bot.py
```

## Security

Never commit `.env` or your real Discord token to GitHub.

## Roadmap

- Live Minecraft server status and online player count.
- Slash commands.
- Better ticket workflow with private threads.
- Staff approval commands for whitelist requests.
