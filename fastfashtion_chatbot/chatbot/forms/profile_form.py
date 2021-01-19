from django.forms import ModelForm
from ..models.customer import CustomerModel


class ProfileForm(ModelForm):

    class Meta:
        model = CustomerModel
        fields = [
            'name', 'birthday', 'email_address',
            'city', 'district', 'street_address'
        ]
