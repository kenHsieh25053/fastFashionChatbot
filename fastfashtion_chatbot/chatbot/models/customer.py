from django.db import models
from django.core.validators import validate_email
import uuid


class CustomerModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    line_channel_id = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=30)
    birthday = models.DateField()
    email = models.EmailField(validators=[validate_email])
    county = models.CharField(max_length=10)
    zipcode = models.CharField(max_length=10, default='000')
    district = models.CharField(max_length=10)
    street_address = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'customer'
        ordering = ['-created_at']
