
from django.core.mail import send_mail
from django.conf import settings


def sending_mail(mailing_setting):
    clients = mailing_setting.client.all()
    email_list = [client.email for client in clients]
    message = mailing_setting.message
    send_mail(
        subject=message.subject,
        message=message.message_content,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=email_list,
        fail_silently=False,
    )
