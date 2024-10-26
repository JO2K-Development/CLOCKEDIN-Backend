# utils.py

from django.conf import settings
from django.core.mail import send_mail


def send_general_email(
    subject: str, message: str, recipient_list: list[str], from_email=None, fail_silently=False, html_message=None
) -> None:
    if from_email is None:
        from_email = settings.DEFAULT_FROM_EMAIL

    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        fail_silently=fail_silently,
        html_message=html_message,
    )
