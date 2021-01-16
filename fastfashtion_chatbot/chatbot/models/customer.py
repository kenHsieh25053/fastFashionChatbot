from django.db import models
from django.core.validators import validate_email
import uuid


class CustomerModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    line_channel_id = models.CharField(max_length=50)
    name = models.CharField(max_length=30)
    birthday = models.DateField()
    email_address = models.EmailField(validators=[validate_email])
    city = models.CharField(max_length=10)
    region = models.CharField(max_length=10)
    street_address = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
