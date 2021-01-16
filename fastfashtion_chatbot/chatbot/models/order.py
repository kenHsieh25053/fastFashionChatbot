from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
import uuid
import datetime

from .customer import Customer


class OrderModel(models.Model):

    PAYMENT_TERMS = (
        ('CREDITCARD', 'CREDITCARD'),
        ('ATM', 'ATM')
    )

    SHIPMENTS = (
        ('711', '711'),
        ('FAMILYMART', 'FAMILYMART'),
        ('DELIVERY', 'DELIVERY')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    items = models.JSONField()
    payment_term = models.CharField(max_length=10, choices=PAYMENT_TERMS)
    shipment = models.CharField(max_length=10, choices=SHIPMENTS)
    shopping_fee = models.IntegerField(validators=[MinValueValidator(0)])
    shipping_date = models.DateTimeField(default=timezone.now)
    shipping_address = models.CharField(max_length=200)
    shipping_address_store = models.CharField(max_length=50)
    total = models.IntegerField(validators=[MinValueValidator(0)])
    paid = models.BooleanField(default=False)
    shipped = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
