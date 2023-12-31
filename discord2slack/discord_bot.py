import os
import discord
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

# .envファイルから環境変数を読み込みます
load_dotenv()

SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
DISCORD_BOT_TOKEN = os.environ['DISCORD_BOT_TOKEN']
DISCORD_CHANNEL_ID = os.environ['DISCORD_CHANNEL_ID']
SLACK_CHANNEL_ID = os.environ['SLACK_CHANNEL_ID']

slack_client = WebClient(token=SLACK_BOT_TOKEN)
intents = discord.Intents(messages=True)
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if str(message.channel.id) == DISCORD_CHANNEL_ID:
        try:
            discord_username = message.author.name
            content = message.clean_content
            print(content)
            slack_message = f"*{discord_username} (Discord)*\n {content}"
            response = slack_client.chat_postMessage(channel=SLACK_CHANNEL_ID, text=slack_message)
        except SlackApiError as e:
            print(f"Error: {e}")

client.run(DISCORD_BOT_TOKEN)