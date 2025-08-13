from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Notification

@shared_task
def send_notification_email(user_email, subject, message):
    """
    Send notification email asynchronously.
    """
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=False,
    )

@shared_task
def create_and_send_notification(user_id, notification_type, message):
    """
    Create a notification in the database and send an email.
    """
    from django.contrib.auth import get_user_model
    User = get_user_model()
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return False

    # Create DB notification
    Notification.objects.create(
        user=user,
        notification_type=notification_type,
        message=message
    )

    # Send email
    send_notification_email.delay(
        user.email,
        f"New Notification: {notification_type}",
        message
    )
    return True
