from django.db import models
import uuid

from .customer import Customer


class WishlistModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    items = models.JSONField()  # name, size, quantity, price
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
