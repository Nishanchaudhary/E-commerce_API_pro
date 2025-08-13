from django.db import models
from django.conf import settings

class Payment(models.Model):
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    provider = models.CharField(max_length=50)  # khalti, stripe...
    provider_id = models.CharField(max_length=255, blank=True, null=True)  # transaction id
    created_at = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=False)
    raw_response = models.JSONField(null=True, blank=True)
