from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('LgAQzKHeSHM8kGI7HPXEjp+UeX1bARwaxUEB2YzCkEs6oOgN42LCbtLU8sH2A+MiespkjrJYeE9qK9D12bhewHzhp1+f+tpMFegUL1+NRKncrxqbMJ2q+Sg2QcbYpUdB3j7vc8cwEbV0XmfREoLx5AdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('80ceab3ed9372169dfd0e1e67bfa6d50')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()