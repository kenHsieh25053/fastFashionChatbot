from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import validate_ipv4_address, validate_ipv6_address, \
    validate_ipv46_address, MinValueValidator
import uuid

from .category import CategoryModel


class ProductModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=20)
    price = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    inventory = models.JSONField()  # size, quantity
    in_stock = models.BooleanField(default=True)
    description = models.TextField(max_length=600)
    image_urls = ArrayField(models.URLField(
        validators=[validate_ipv4_address, validate_ipv6_address, validate_ipv46_address]))
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category_id = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)

    class Meta:
        db_table = 'product'
        ordering = ['-created_at']
