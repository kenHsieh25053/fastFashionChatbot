from django.conf import settings
from django.http import (
    HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
)
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.template.response import TemplateResponse
from django.views import View

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from .services.customer import Customer
from .message import MessageHandler
from .forms.profile_form import ProfileForm
from .models import CustomerModel

import datetime

from .message_templates import PROFILE_MESSAGE

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


PROFILE_BUTTONS = [
    {'label': '新增/修改個資',  'data': 'update/edit_profile'},
    {'label': '近三個月購買歷史',  'data': 'order_history_3m'}
]

LIFF_PROFILE_FORM_URL = 'https://liff.line.me/1655603396-pm1nzwnE?data='
customer = Customer()
messageHandler = MessageHandler()


@method_decorator(csrf_exempt, name='dispatch')
class LineMessageController(View):

    def post(self, request):

        # get X-Line-Signature header value
        signature = request.META['HTTP_X_LINE_SIGNATURE']

        # get request body as text
        body = request.body.decode('utf-8')

        # handle webhook body
        try:
            event = parser.parse(body, signature)[0]
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
                messageHandler.reply_quickreply_message(
                    PROFILE_BUTTONS, event)
                # self.customer.save_profile(event, line_channel_id)
            elif event.message.text == 'wishlist':
                pass
            elif event.message.text == 'shoppingCart':
                pass
            elif event.message.text == 'customerServices':
                pass
            else:
                text = '抱歉，我不了解您的問題'
                messageHandler.reply_text_message(event, text)
        else:
            if event.postback.data == 'update/edit_profile':
                # data = f'請填寫個人資料表單 {LIFF_PROFILE_FORM_URL}'
                data = f'請填寫個人資料表單 {LIFF_PROFILE_FORM_URL}{line_channel_id}'
                messageHandler.reply_postback_message(event, data)
            else:
                data = 'through liff'
                messageHandler.reply_postback_message(event, data)


# {"mode": "active", "postback": {"data": "update/edit_profile"}, "replyToken": "22768e4f3ba64a50b5dfd16899e0c292",
#     "source": {"type": "user", "userId": "Uce9d1340f1730e26212eacf2a27c7ba0"}, "timestamp": 1610885128612, "type": "postback"}

class ProfileController(View):

    def get(self, request, userid):
        line_channel_id = request.GET.get('data')
        if line_channel_id:
            instance = get_object_or_404(
                CustomerModel.objects, line_channel_id=line_channel_id)
            birthday = datetime.datetime.strftime(
                instance.__dict__['birthday'], '%Y-%m-%d')
            profile = {
                'name': instance.__dict__['name'],
                'email': instance.__dict__['email'],
                'birthday': birthday,
                'county': instance.__dict__['county'],
                'zipcode': instance.__dict__['zipcode'],
                'district': instance.__dict__['district'],
                'street_address': instance.__dict__['street_address']
            }
            form = ProfileForm(initial=profile)
        else:
            form = ProfileForm()

        return render(request, 'profile-form.html', {'form': form})

    def post(self, request):
        line_channel_id = request.POST['line_channel_id']
        instance = get_object_or_404(
            CustomerModel, line_channel_id=line_channel_id)
        form = ProfileForm(request.POST, instance=instance)
        if form.is_valid():
            if instance:
                form = ProfileForm(request.POST, instance=instance)
            else:
                form = ProfileForm()
            form.save()
        else:
            return HttpResponseBadRequest()

        return TemplateResponse(request, 'thanks.html', {})
