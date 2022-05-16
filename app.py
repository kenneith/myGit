import os
import requests
import json

from datetime import datetime

from flask import Flask, abort, request

# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))


@app.route("/", methods=["GET", "POST"])
def callback():

    if request.method == "GET":
        return "Hello Heroku"
    if request.method == "POST":
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)

        return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    get_message = event.message.text
    
    url = "https://aispapi_test.hamastar.com.tw/api/v3/model_test/ABUxIKSFYMEw6ZSUHxF4WA@@/yuykH9slI5prrpqvpS1U7Q@@"

    payload = json.dumps({
        "articles": [
            {
                "Question": get_message
                }
            ]
        })
    headers = {
        'Content-Type': 'application/json',
        'Cookie': '_culture=zh-TW'
        }

    response = requests.request("POST", url, headers=headers, data=payload)


    # Send To Line
    # reply = TextSendMessage(text=f"{get_message}")
    reply = TextSendMessage(text=f"{response.text}")
    line_bot_api.reply_message(event.reply_token, reply)

