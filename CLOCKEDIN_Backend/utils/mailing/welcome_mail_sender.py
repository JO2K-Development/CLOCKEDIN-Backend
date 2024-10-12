from django.http import HttpResponse

from CLOCKEDIN_Backend.utils.mailing.mail_sender import send_general_email


def send_welcome_email(recipient: str):
    subject = f"Welcome to Our Platform!"
    message = "Thank you for registering on our platform. We're glad to have you!"

    html_message = "<h1>Welcome</h1><p>Thank you for registering on our platform. We're glad to have you!</p>"

    send_general_email(subject, message, [recipient], html_message=html_message)
    return HttpResponse("Email sent successfully!")
