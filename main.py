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

print(f"Relaying messages from Discord channel {DISCORD_CHANNEL_ID} to {WEBHOOK_URL}")


@client.event
async def on_message(message):

    if str(message.channel.id) != DISCORD_CHANNEL_ID:
        return

    print(f"Realying message from user {message.author.name}: {message.content}")

    headers = {}  # TODO: make customizable

    res = requests.post(url=WEBHOOK_URL, json=message, headers=headers)

    if not res.ok:
        print(res.text)


client.run(DISCORD_BOT_TOKEN)
