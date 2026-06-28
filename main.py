import discord
from dotenv import load_dotenv
from os import getenv
import requests

load_dotenv()

DISCORD_BOT_TOKEN = getenv("DISCORD_BOT_TOKEN", "")
DISCORD_CHANNEL_ID = getenv("DISCORD_CHANNEL_ID")

WEBHOOK_URL = getenv("WEBHOOK_URL", "http://localhost:8080/webhook")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

print(f"Relaying messages from Discord to {WEBHOOK_URL}")

if DISCORD_CHANNEL_ID:
    print(f"Ignoring messages from channels other than {DISCORD_CHANNEL_ID}")


@client.event
async def on_message(message):

    if DISCORD_CHANNEL_ID and str(message.channel.id) != DISCORD_CHANNEL_ID:
        return

    headers = {}  # TODO: make customizable

    json = {
        "id": str(message.id),
        "content": message.content,
        "author": {
            "id": str(message.author.id),
            "name": message.author.name,
            "discriminator": message.author.discriminator,
        },
        "channel_id": str(message.channel.id),
        "guild_id": str(message.guild.id) if message.guild else None,
        "created_at": message.created_at.isoformat(),
    }

    res = requests.post(url=WEBHOOK_URL, json=json, headers=headers)

    if not res.ok:
        print(res.text)


client.run(DISCORD_BOT_TOKEN)
