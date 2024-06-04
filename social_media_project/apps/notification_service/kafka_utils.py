# notification_service/kafka_utils.py
import logging
from confluent_kafka import Producer, Consumer, KafkaError
from django.core.mail import send_mass_mail, send_mail
from django.conf import settings
import json
from ..user_service.models import User
from django.http import HttpResponse
from django.utils.html import strip_tags
from django.template.loader import render_to_string

logging.basicConfig(level=logging.DEBUG)

KAFKA_SERVER = '127.0.0.1:9092'
KAFKA_TOPIC = 'notifications'

producer = Producer({'bootstrap.servers': KAFKA_SERVER})

def send_notification_to_kafka(message):
    serialized_message = json.dumps(message).encode('utf-8')  # Serialize and encode the message
    producer.produce(KAFKA_TOPIC, serialized_message)
    producer.flush()

consumer = Consumer({
    'bootstrap.servers': KAFKA_SERVER,
    'group.id': 'notification_group',
    'auto.offset.reset': 'earliest'
})

consumer.subscribe([KAFKA_TOPIC])

def consume_notifications():
    # import pdb
    # pdb.set_trace()
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(msg.error())
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                logging.error(msg.error())
                break
        logging.info(f"Message consum----------------ed: {msg.value().decode('utf-8')}")
        # import pdb
        # pdb.set_trace()
        handle_notification(msg.value().decode('utf-8'))

def handle_notification(message):
    message_data = {
    'type': 'post',
    'receiver_id': 'salmanyagaka@gmail.com',
    'message': 'New post created with title: My Awesome Post'
}
    receiver_emails = User.objects.filter(is_active=True).values_list('email', flat=True)

    # import pdb
    # pdb.set_trace()

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