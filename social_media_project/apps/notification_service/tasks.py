from celery import shared_task
from django.core.mail import send_mass_mail, EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail, send_mass_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import html2text

from .models import Notification
from social_media_project.apps.user_service.models import User

import math

BATCH_SIZE = 100 


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

            context.update(context)
            context["message"] = message
            context["notification"] = notification
            html_content = render_to_string(html_template, context)
            text_content = html2text.html2text(html_content)

            email_messages.append(
                (
                    subject,
                    text_content,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    html_content,
                )
            )

        # Send emails in bulk
        send_bulk_emails(email_messages)

    return f"Notifications sent to {total_users} users in {num_batches} batches."


def send_bulk_emails(email_messages):
    connection = get_connection()
    emails = []
    for (
        subject,
        text_content,
        from_email,
        recipient_list,
        html_content,
    ) in email_messages:
        email = EmailMultiAlternatives(
            subject, text_content, from_email, recipient_list, connection=connection
        )
        email.attach_alternative(html_content, "text/html")
        emails.append(email)
    connection.send_messages(emails)
