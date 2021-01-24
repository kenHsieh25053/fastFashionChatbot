from django.conf import settings

from linebot import LineBotApi
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, \
    QuickReply, QuickReplyButton, PostbackAction


line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)


class MessageHandler():

    def __init__(self):
        pass

    def reply_text_message(self, event, text):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text)
        )

    def reply_quickreply_message(self, buttons, event):
        quick_reply_messages = []
        for button in buttons:
            quick_reply_button = QuickReplyButton(action=PostbackAction(
                label=button['label'], display_text=button['label'], data=button['data']))
            quick_reply_messages.append(quick_reply_button)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='請選擇以下選項',
                            quick_reply=QuickReply(items=quick_reply_messages))
        )

    def reply_postback_message(self, event, data):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=data)
        )

    def reply_flex_message(self, event):
        pass
