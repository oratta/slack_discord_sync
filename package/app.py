import os
import awsgi
from flask import Flask, request, jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from discord import Webhook, RequestsWebhookAdapter

app = Flask(__name__)

# Slack APIクライアントの初期化
slack_client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])

# DiscordのWebhook URL
discord_webhook_url = os.environ["DISCORD_WEBHOOK_URL"]
discord_webhook = Webhook.from_url(discord_webhook_url, adapter=RequestsWebhookAdapter())

def lambda_handler(event, context):
    return awsgi.response(app, event, context)

@app.route("/slack", methods=["POST"])
def handle_slack_webhook():
    payload = request.json

    if payload["event"]["type"] == "message" and "subtype" not in payload["event"]:
        channel_id = payload["event"]["channel"]
        message = payload["event"]["text"]

        # SlackメッセージをDiscordに送信
        discord_webhook.send(content=message)

    return jsonify({"status": "success"})

@app.route("/discord", methods=["POST"])
def handle_discord_webhook():
    payload = request.json
    content = payload["content"]
    channel_id = payload["channel_id"]

    # DiscordメッセージをSlackに送信
    try:
        response = slack_client.chat_postMessage(channel=channel_id, text=content)
    except SlackApiError as e:
        print(f"Error: {e}")

    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(port=3000)