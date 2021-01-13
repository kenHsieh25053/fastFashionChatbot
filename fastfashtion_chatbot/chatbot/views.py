from django.conf import settings
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View

from linebot import LineBotApi, WebhookHandler, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


@method_decorator(csrf_exempt, name='dispatch')
class Handler(View):

    def post(self, request):

        # get X-Line-Signature header value
        signature = request.META['HTTP_X_LINE_SIGNATURE']

        # get request body as text
        body = request.body.decode('utf-8')

        # handle webhook body
        try:
            events = parser.parse(body, signature)
            print(events)
            self.__handle_messages(events[0])
        except InvalidSignatureError as error:
            print(error)
            return HttpResponseBadRequest()
        except LineBotApiError as error:
            print(error)
            return HttpResponseBadRequest()

        return HttpResponse()

    def __handle_messages(self, event):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )
