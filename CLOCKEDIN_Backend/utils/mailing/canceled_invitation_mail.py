from django.http import HttpResponse

from CLOCKEDIN_Backend.utils.mailing.mail_sender import send_general_email


def send_cancelled_invitation_email(recipient: str):
    subject = f"Invitation has been cancelled"
    message = "There was an invitation for you, but it has been cancelled."

    html_message = "<h1>Welcome</h1><p>There used to be an invitation for you, but it has been cancelled!</p>"

    send_general_email(subject, message, [recipient], html_message=html_message)
    return HttpResponse("Email sent successfully!")
