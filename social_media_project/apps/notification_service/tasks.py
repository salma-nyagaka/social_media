from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail, send_mass_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import Notification


from social_media_project.apps.user_service.models import User


@shared_task
def send_email_task(
    subject,
    message,
    from_email,
    recipient_list,
    html_template=None,
    context=None,
    bcc=None,
):
    if html_template:
        if context is None:
            context = {}
        context["message"] = message
        html_content = render_to_string(html_template, context)
        text_content = strip_tags(html_content)
    else:
        html_content = message
        text_content = strip_tags(message)

    email = EmailMultiAlternatives(
        subject, text_content, from_email, recipient_list, bcc=bcc
    )
    if html_template:
        email.attach_alternative(html_content, "text/html")

    email.send()


# from .models import User
import math

BATCH_SIZE = 100  # Adjust batch size as needed


@shared_task
def send_batch_notifications(
    subject, message, recipient_list, context, html_template, notification_type
):
    user_emails = recipient_list
    total_users = len(user_emails)
    num_batches = math.ceil(total_users / BATCH_SIZE)

    for batch_num in range(num_batches):
        batch_emails = user_emails[
            batch_num * BATCH_SIZE : (batch_num + 1) * BATCH_SIZE
        ]
        email_messages = []

        for email in batch_emails:
            user_obj = User.objects.get(email=email)
            # Save notification to the database
            notification = Notification.objects.create(
                sender=settings.DEFAULT_FROM_EMAIL,
                receiver=user_obj,
                notification_type=notification_type,  # Adjust as needed
                text=message,
            )

            user = User.objects.get(email=email)
            context.update(context)
            html_content = render_to_string(html_template, context)
            text_content = strip_tags(html_content)
            email_messages.append(
                (subject, text_content, settings.DEFAULT_FROM_EMAIL, [email])
            )

        send_mass_mail(tuple(email_messages), fail_silently=False)
