from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin','Admin'),
        ('seller','Seller'),
        ('customer','Customer'),
        ('delivery','DeliveryPartner'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    phone_number = models.CharField(max_length=20, blank=True, null=True)

class DeviceSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='device_sessions')
    device_id = models.CharField(max_length=255)
    user_agent = models.CharField(max_length=512, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    revoked = models.BooleanField(default=False)

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=8)
    purpose = models.CharField(max_length=32, default='login')
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
