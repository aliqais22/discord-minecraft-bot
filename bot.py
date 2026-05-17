import os

import discord
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
SERVER_IP = os.getenv("MINECRAFT_SERVER_IP", "play.example.com")
SERVER_VERSION = os.getenv("MINECRAFT_VERSION", "1.20+")
STAFF_CHANNEL_ID = os.getenv("STAFF_CHANNEL_ID")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


def build_help_message():
    return (
        "**MineBot Commands**\n"
        "`!hello` - test the bot\n"
        "`!ping` - check the bot latency\n"
        "`!mc` - show Minecraft server info\n"
        "`!rules` - show server rules\n"
        "`!whitelist <minecraft_name>` - request whitelist access\n"
        "`!ticket <message>` - ask the staff for help\n"
        "`!about` - info about the bot"
    )


async def send_to_staff(guild, embed):
    if not guild or not STAFF_CHANNEL_ID:
        return False

    try:
        channel_id = int(STAFF_CHANNEL_ID)
    except ValueError:
        print("STAFF_CHANNEL_ID must be a Discord channel ID number.")
        return False

    channel = guild.get_channel(channel_id)
    if not channel:
        try:
            channel = await client.fetch_channel(channel_id)
        except discord.DiscordException:
            return False

    try:
        await channel.send(embed=embed)
    except discord.DiscordException:
        return False

    return True


@client.event
async def on_ready():
    print(f"Bot is online as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user or message.author.bot:
        return

    content = message.content.strip()
    lowered = content.lower()

    if lowered == "!hello":
        await message.channel.send("Hello! MineBot is ready.")

    elif lowered == "!help":
        await message.channel.send(build_help_message())

    elif lowered == "!ping":
        latency_ms = round(client.latency * 1000)
        await message.channel.send(f"Pong! `{latency_ms}ms`")

    elif lowered == "!about":
        await message.channel.send(
            "I am MineBot, a Discord assistant for a Minecraft community."
        )

    elif lowered == "!mc":
        embed = discord.Embed(
            title="Minecraft Server",
            description="Server information for the community.",
            color=discord.Color.green(),
        )
        embed.add_field(name="IP", value=f"`{SERVER_IP}`", inline=True)
        embed.add_field(name="Version", value=f"`{SERVER_VERSION}`", inline=True)
        embed.add_field(
            name="Status",
            value="Manual for now. Live status is the next feature.",
            inline=False,
        )
        await message.channel.send(embed=embed)

    elif lowered == "!rules":
        await message.channel.send(
            "**Server Rules**\n"
            "1. Respect other players.\n"
            "2. No griefing or stealing.\n"
            "3. No cheats, hacks, or unfair mods.\n"
            "4. Keep chat friendly.\n"
            "5. Listen to staff decisions."
        )

    elif lowered.startswith("!whitelist"):
        parts = content.split(maxsplit=1)
        if len(parts) == 1:
            await message.channel.send("Use: `!whitelist <minecraft_name>`")
            return

        minecraft_name = parts[1].strip()
        embed = discord.Embed(
            title="Whitelist Request",
            color=discord.Color.gold(),
        )
        embed.add_field(name="Discord User", value=message.author.mention, inline=False)
        embed.add_field(name="Minecraft Name", value=f"`{minecraft_name}`", inline=False)
        embed.add_field(name="Channel", value=message.channel.mention, inline=False)

        sent_to_staff = await send_to_staff(message.guild, embed)
        response = (
            f"Whitelist request received for `{minecraft_name}`. Staff will review it."
            if sent_to_staff
            else f"Whitelist request saved here for `{minecraft_name}`. Add `STAFF_CHANNEL_ID` to forward it to staff."
        )
        await message.channel.send(response)

    elif lowered.startswith("!ticket"):
        parts = content.split(maxsplit=1)
        if len(parts) == 1:
            await message.channel.send("Use: `!ticket <your message>`")
            return

        ticket_message = parts[1].strip()
        embed = discord.Embed(
            title="Support Ticket",
            description=ticket_message,
            color=discord.Color.blue(),
        )
        embed.add_field(name="Discord User", value=message.author.mention, inline=False)
        embed.add_field(name="Channel", value=message.channel.mention, inline=False)

        sent_to_staff = await send_to_staff(message.guild, embed)
        response = (
            f"Ticket received from {message.author.mention}. Staff will help soon."
            if sent_to_staff
            else "Ticket saved here. Add `STAFF_CHANNEL_ID` to forward it to staff."
        )
        await message.channel.send(response)


if not TOKEN:
    raise RuntimeError("Missing DISCORD_TOKEN. Add it to a .env file first.")

client.run(TOKEN)
