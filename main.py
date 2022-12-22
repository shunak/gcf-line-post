import os
import base64, hashlib, hmac
import logging
import urllib.request,requests, json

from flask import abort, jsonify

from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)

def main(request):
    channel_secret = os.environ.get('LINE_CHANNEL_SECRET')
    channel_access_token = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
    news_json_url = os.environ.get('NEWS_JSON_URL')

    line_bot_api = LineBotApi(channel_access_token)
           
    url = requests.get(news_json_url)
    json_text = url.text
    contents = json.loads(json_text)
    chat_text=""

    for (i,content) in enumerate(contents):
        chat_text += content["topic"] + "\n" + content["url"] + "\n"
        articles = TextSendMessage(text=chat_text)

    line_bot_api.broadcast(articles)

    return jsonify({ 'message': 'ok'})
