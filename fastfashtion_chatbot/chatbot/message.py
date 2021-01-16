from django.conf import settings

from linebot import LineBotApi
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, QuickReply


line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)


class MessageHandler():

    def __init__(self, event):
        self.event = event

    def reply_text_message(self, event):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )

    def reply_quickreply_message(self, event, items):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='選擇地點查詢開啟google map, 或是選擇其他主題分類',
                            quick_reply=QuickReply(items=items))
        )

    def reply_postback_message(self, event):
        pass
