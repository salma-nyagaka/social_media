# notification_service/management/commands/start_consumer.py
from django.core.management.base import BaseCommand
from social_media_project.apps.notification_service.kafka_utils import consume_notifications

class Command(BaseCommand):
    help = 'Starts the Kafka consumer for notifications'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting Kafka consumer...'))
        consume_notifications()