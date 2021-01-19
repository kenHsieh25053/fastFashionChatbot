from django.core.cache import cache
from ..models import CustomerModel

import json


class Customer():

    def __init__(self):
        pass

    def get_profile(self, line_channel_id):
        profile = CustomerModel.objects.get(line_channel_id=line_channel_id)
        return profile

    def save_profile(self, event, line_channel_id):
        profile = event.postback.data.split('_')[1]
        key = event.postback.data.split('_')[0] + line_channel_id
        data = cache.get(key)
        if data:
            data = json.load(data)
            data.update(profile)
            cache.set(key, data)
        else:
            data = json.dump(profile)
            cache.set(key, profile)

        return
