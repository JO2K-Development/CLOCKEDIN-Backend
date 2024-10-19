from django.http import HttpResponse

from CLOCKEDIN_Backend.utils.mailing.mail_sender import send_general_email


def send_verification_email(recipient: str, verification_link: str):
    subject = f"Verify your email"
    message = f"Please click the following link to verify your email: {verification_link}"

    html_message = f"<h1>Verify your email</h1><p>Please click the following link to verify your email: <a href='{verification_link}'>{verification_link}</a></p>"

    send_general_email(subject, message, [recipient], html_message=html_message)
    return HttpResponse("Email sent successfully!")