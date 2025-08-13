# orders/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from notifications.tasks import create_and_send_notification

@receiver(post_save, sender=Order)
def order_created_notification(sender, instance, created, **kwargs):
    if created:
        create_and_send_notification.delay(
            instance.user.id,
            'order_created',
            f"Your order #{instance.id} has been placed successfully."
        )
