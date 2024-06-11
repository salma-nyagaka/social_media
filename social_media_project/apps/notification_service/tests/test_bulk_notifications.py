import pytest
from django.core import mail
from django.conf import settings
from social_media_project.apps.notification_service.tasks import (
    send_batch_notifications,
    send_bulk_emails,
)
from social_media_project.apps.notification_service.models import Notification
from social_media_project.apps.user_service.models import User
from rest_framework.test import APIClient
import html2text


@pytest.mark.django_db
class TestNotificationTasks:
    @pytest.fixture(autouse=True)
    def setup_method(self, db):
        """
        Setup method to create test users and initialize the test client.
        This fixture is run before each test method.
        """
        self.client = APIClient()
        self.users = [
            User.objects.create(
                username=f"user{i}", email=f"user{i}@example.com", is_active=True
            )
            for i in range(5)
        ]
        self.user_emails = [user.email for user in self.users]
        self.context = {"extra_info": "Additional information"}

    def test_send_batch_notifications(self):
        """
        Test the send_batch_notifications function.
        This test verifies that the correct number of notifications are created
        and emails are sent with the expected content.
        """
        subject = "Test Subject"
        message = "Test Message"
        html_template = "follow.html"
        notification_type = "follow"

        # Call the task to send batch notifications
        result = send_batch_notifications(
            subject,
            message,
            self.user_emails,
            self.context,
            html_template,
            notification_type,
        )

        # Assert that the result is as expected
        assert result == "Notifications sent to 5 users in 1 batches."

        # Verify that notifications are created for each user
        assert Notification.objects.count() == len(self.user_emails)

        # Verify that emails are sent for each user
        assert len(mail.outbox) == len(self.user_emails)

        # Check the content of each email
        for email in mail.outbox:
            expected_text = "# New follower alert!\n\nTest Message\n\nThank you for being a valued member of our community."
            assert (
                html2text.html2text(email.alternatives[0][0]).strip() == expected_text
            )

    def test_send_bulk_emails(self):
        """
        Test the send_bulk_emails function.
        This test verifies that the correct number of emails are sent
        with the expected content.
        """
        email_messages = [
            ("Subject 1", "Text 1", "from@example.com", ["to1@example.com"], "HTML 1"),
            ("Subject 2", "Text 2", "from@example.com", ["to2@example.com"], "HTML 2"),
        ]

        # Call the function to send bulk emails
        send_bulk_emails(email_messages)

        # Verify that the correct number of emails are sent
        assert len(mail.outbox) == len(email_messages)

        # Check the content of each email
        for email, (_, text_content, _, _, html_content) in zip(
            mail.outbox, email_messages
        ):
            assert email.body == text_content
            assert email.alternatives[0][0] == html_content
            assert email.alternatives[0][1] == "text/html"
