from django.conf import settings
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

from django.views import View

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from .services.customer import Customer
from .message import MessageHandler
from .forms.profile_form import ProfileForm

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


PROFILE_BUTTONS = [
    {'label': '新增/修改個資',  'data': 'update/edit_profile'},
    {'label': '近三個月購買歷史',  'data': 'order_history_3m'}
]

PROFILE_FORM_URL = settings.DOMAIN + '/chatbot/profile-form'


@method_decorator(csrf_exempt, name='dispatch')
class LineMessageController(View):

    def __init__(self):
        self.customer = Customer()
        self.messageHandler = MessageHandler()

    def post(self, request):

        # get X-Line-Signature header value
        signature = request.META['HTTP_X_LINE_SIGNATURE']

        # get request body as text
        body = request.body.decode('utf-8')

        # handle webhook body
        try:
            event = parser.parse(body, signature)[0]
            print(event)
            self.__dispatch_messages(event)
        except InvalidSignatureError as error:
            print(error)
            return HttpResponseBadRequest()
        except LineBotApiError as error:
            print(error)
            return HttpResponseBadRequest()

        return HttpResponse()

    def __dispatch_messages(self, event):
        line_channel_id = event.source.user_id
        if event.type == 'message':
            if event.message.text == 'latest':
                pass
            elif event.message.text == 'search':
                pass
            elif event.message.text == 'profile':
                self.messageHandler.reply_quickreply_message(
                    PROFILE_BUTTONS, event)
                # self.customer.save_profile(event, line_channel_id)
            elif event.message.text == 'wishlist':
                pass
            elif event.message.text == 'shoppingCart':
                pass
            elif event.message.text == 'customerServices':
                pass
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='對不起，我不了解您的問題')
                )
        else:
            if event.postback.data == 'update/edit_profile':
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=f'請填寫個人資料表單 {PROFILE_FORM_URL}')
                )


# {"mode": "active", "postback": {"data": "update/edit_profile"}, "replyToken": "22768e4f3ba64a50b5dfd16899e0c292",
#     "source": {"type": "user", "userId": "Uce9d1340f1730e26212eacf2a27c7ba0"}, "timestamp": 1610885128612, "type": "postback"}

class ProfileController(View):

    form = ProfileForm()

    def get(self, request):
        context = {
            'form': self.form
        }
        return render(request, 'profile-form.html', context)

    def post(self, request):
        pass
