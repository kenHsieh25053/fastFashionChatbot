from django.core.cache import cache
from ..models import CustomerModel


class Customer():

    def __init__(self, line_channel_id, event):
        self.line_channel_id = line_channel_id
        self.event = event

    def get_profile(self, line_channel_id):
        profile = CustomerModel.objects.get(line_channel_id=line_channel_id)
        return profile

    def save_profile(self, event, line_channel_id):
        cache.set(line_channel_id)
