from django.db import models
import uuid
from django.contrib.auth import get_user_model  # Import the custom user model

class Credential(models.Model):
    PLATFORM_TYPES = [
        ('binance', 'Binance'),
        ('oanda', 'Oanda'),
        ('alpace', 'Alpace'),
    ]
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)  # Use get_user_model() to reference the custom user model
    api_key = models.CharField(max_length=255)
    secret_key = models.CharField(max_length=255)
    unique_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    platform_type = models.CharField(max_length=30, choices=PLATFORM_TYPES, default='binance')

    def __str__(self):
        return f"{self.user.username}'s Credentials"



class Order(models.Model):
    ORDER_TYPE_CHOICES = [
        ('Market', 'market'),
    ]

    ORDER_ACTION_CHOICES = [
        ('Buy', 'buy'),
        ('Sell', 'sell'),
    ]

    PRICE_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('FILLED', 'Filled'),
        ('PARTIALLY_FILLED', 'Partially Filled'),
        ('CANCELLED', 'Cancelled'),
    ]

    PLATFORM_TYPES = [
        ('binance', 'Binance'),
        ('oanda', 'Oanda'),
        ('alpace', 'Alpace'),
    ]

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    order_type = models.CharField(max_length=10, choices=ORDER_TYPE_CHOICES)
    symbol = models.CharField(max_length=30,default='')
    order_action = models.CharField(max_length=10, choices=ORDER_ACTION_CHOICES)
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    price = models.DecimalField(max_digits=12, decimal_places=8)
    status = models.CharField(max_length=16, choices=PRICE_STATUS_CHOICES)
    platform_type = models.CharField(max_length=10, choices=PLATFORM_TYPES)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order ID: {self.id}, User: {self.user.username}, Type: {self.order_type}, Action: {self.order_action}, Status: {self.status}"