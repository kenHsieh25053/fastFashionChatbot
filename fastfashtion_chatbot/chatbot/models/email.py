from django.db import models
from django.core.validators import validate_email
import uuid

from .customer import CustomerModel


class EmailModel(models.Model):

    EMAIL_TYPES = (
        ('ORDER', 'ORDER'),
        ('RECEIPT', 'RECEIPT'),
        ('MARKETING', 'MARKETING'),
        ('INFO', 'INFO')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=15, choices=EMAIL_TYPES)
    receiver = models.CharField(max_length=20)
    email = models.EmailField(validators=[validate_email])
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(CustomerModel, on_delete=models.CASCADE)

    class Meta:
        db_table = 'email'
        ordering = ['-created_at']
