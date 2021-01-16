from django.conf import settings
from django.core.checks import messages
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import json

from .helpers import customer
from .message import MessageHandler

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


@method_decorator(csrf_exempt, name='dispatch')
class Controller(View):

    def __init__(self):
        self.customer = customer.Customer()
        self.messageHandler = MessageHandler()

    def post(self, request):

        # get X-Line-Signature header value
        signature = request.META['HTTP_X_LINE_SIGNATURE']

        # get request body as text
        body = request.body.decode('utf-8')

        # handle webhook body
        try:
            event = parser.parse(body, signature)[0]
            if event.type == 'text':
                if event
                MessageHandler.reply_text_message(event)
            else:
                self.__handle_postback_actions(event)
        except InvalidSignatureError as error:
            print(error)
            return HttpResponseBadRequest()
        except LineBotApiError as error:
            print(error)
            return HttpResponseBadRequest()

        return HttpResponse()

    def __handle_messages(self, event):
        if event.message.type == 'location':
            pass
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=event.message.text)
            )

    def __handle_postback_actions(self, event):
        action_type = event.postback.data.split('_')[0]
        line_channel_id = event.source.user_id
        if action_type == 'customer':
            self.__handle_customer_postback_action(event, line_channel_id)

    '''
    add name
    add birthday
    add email
    add city
    add region
    add street_address
    '''

    def __handle_customer_postback_action(self, event, line_channel_id):
        action = event.postback.data.split('_')[1]
        text_message = f'請輸入{action}'

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text_message)
        )

        customer.save_profile(event.postback, line_channel_id)
