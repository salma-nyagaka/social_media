# notification_service/views.py
from rest_framework import viewsets
from .models import Notification

# views.py
from django.core.mail import send_mail, send_mass_mail
from django.http import HttpResponse
from django.utils.html import strip_tags
import logging
import json
from django.template.loader import render_to_string

from ..user_service.models import User

from .tasks import send_email_task
from .serializers import NotificationSerializer

# from .kafka_utils import send_notification_to_kafka
