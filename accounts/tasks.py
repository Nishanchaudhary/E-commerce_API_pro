from celery import shared_task
from django.core.mail import send_mail
from .models import User

@shared_task
def send_otp_task(user_id, code):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return
    # For production wire SMS via Twilio / SMS gateway. For now use email
    send_mail(
        subject='Your OTP code',
        message=f'Your OTP is {code}',
        from_email='no-reply@ecom.local',
        recipient_list=[user.email] if user.email else [],
        fail_silently=True
    )
