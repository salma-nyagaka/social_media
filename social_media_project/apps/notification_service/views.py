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

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def perform_create(self, serializer):
        notification = serializer.save()
        # send_notification_to_kafka(notification.text)
        

def test_email(request):

    # Logic for your view
    send_email_task.delay(
        'Subject here',
        'Here is the message.',
        'salmanyagaka@gmail.com',
        ['salmanyagaka@gmail.com', 'salmanyagakaws@gmail.com'],
    )
    return HttpResponse('Email sent!')


def test_kafka_notification(request):
    notification_data = {
        'receiver_email': 'salmanyagaka@gmail.com',
        'subject': 'Test Notification',
        'message': 'This is a test notification.'
    }
    # send_notification_to_kafka(notification_data)
    return HttpResponse("Notification sent to Kafka!")
