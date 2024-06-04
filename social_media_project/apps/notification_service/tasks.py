from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from urllib import request
import jwt
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
import django
from django.utils.encoding import force_bytes
from django.conf import settings
import datetime
from django.utils import timezone
from datetime import datetime, timedelta


secret = settings.SECRET_KEY


@shared_task
def send_activation_email(user):
    # uidb64 = urlsafe_base64_encode(force_bytes(user.id))
    payload = {
        "email": user.email,
        "exp": (timezone.now() + timezone.timedelta(hours=24)).timestamp(),
    }

    exp = datetime.utcnow() + timedelta(hours=24)
    token = jwt.encode(
        {"user_id": user.id, "exp": exp}, settings.SECRET_KEY, algorithm="HS256"
    )

    subject = "User Account Activation Request"
    domain = settings.DOMAIN_NAME
    html_message = render_to_string(
        "activation_email.html",
        {"context": "{}/users/email_confirmation/{}".format(domain, str(token))},
    )
    # import pdb
    # pdb.set_trace()
    plain_message = strip_tags(html_message)
    from_email = "salmanyagaka@gmail.com"
    to = user.email

    send_mail(subject, plain_message, from_email, [to], html_message=html_message)


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