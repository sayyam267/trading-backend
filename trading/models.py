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