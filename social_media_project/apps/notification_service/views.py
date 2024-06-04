# notification_service/views.py
from rest_framework import viewsets
from .models import Notification
from .serializers import NotificationSerializer
from .kafka_utils import send_notification_to_kafka

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def perform_create(self, serializer):
        notification = serializer.save()
        send_notification_to_kafka(notification.text)
        
# views.py
from django.core.mail import send_mail, send_mass_mail
from django.http import HttpResponse
from django.utils.html import strip_tags
import logging
import json
from django.template.loader import render_to_string

from ..user_service.models import User
def test_email(self):
    message_data = {
    'type': 'post',
    'receiver_id': 'salmanyagaka@gmail.com',
    'message': 'New post created with title: My Awesome Post'
}
    receiver_emails = User.objects.filter(is_active=True).values_list('email', flat=True)


    try:
        # Create a list of email tuples (subject, message, from_email, recipient_list)
        subject = 'Test Subject'
        context = {'message': message_data['message']}  # Customize context as needed
        html_message = render_to_string('new_post.html', context)
        plain_message = strip_tags(html_message)
        email_messages = [(subject, plain_message, 'salmanyagaka@gmail.com', receiver_emails)]
        send_mass_mail(email_messages)
        
        logging.info(f"Emails sent to {', '.join(receiver_emails)}")
        return HttpResponse("Emails sent successfully")

    except Exception as e:
        logging.error(f"Failed to send emails: {e}")
        return HttpResponse(str(e))



from .kafka_utils import send_notification_to_kafka

def test_kafka_notification(request):
    notification_data = {
        'receiver_email': 'salmanyagaka@gmail.com',
        'subject': 'Test Notification',
        'message': 'This is a test notification.'
    }
    send_notification_to_kafka(notification_data)
    return HttpResponse("Notification sent to Kafka!")
