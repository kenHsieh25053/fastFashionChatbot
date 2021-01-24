from django.forms import ModelForm
from ..models.customer import CustomerModel


class ProfileForm(ModelForm):

    class Meta:
        model = CustomerModel
        fields = [
            'name', 'line_channel_id', 'birthday', 'email',
            'county', 'zipcode', 'district', 'street_address'
        ]
        labels = {
            'name': '姓名',
            'line_channel_id': 'line_channel_id',
            'email': 'email',
            'birthday': '生日',
            'county': '城市',
            'zipcode': '區碼',
            'district': '區',
            'street_address': '地址'
        }
