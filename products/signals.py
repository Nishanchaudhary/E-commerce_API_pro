from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ProductVariant
from notifications.tasks import notify_low_stock

@receiver(post_save, sender=ProductVariant)
def variant_post_save(sender, instance, created, **kwargs):
    if instance.inventory <= instance.low_stock_threshold:
        notify_low_stock.delay(instance.id)
