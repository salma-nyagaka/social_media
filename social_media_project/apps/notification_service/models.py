# notification_service/models.py
from django.db import models
from django.conf import settings


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ("post", "Post"),
        ("comment", "Comment"),
        ("registration", "Registration"),
        ("follow", "Follow"),
        ("unfollow", "Unfollow"),
    )

    sender = models.CharField(
     max_length=100
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="received_notifications",
        on_delete=models.CASCADE,
    )
    notification_type = models.CharField(choices=NOTIFICATION_TYPES, max_length=20)
    text = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} sent a {self.notification_type} notification to {self.receiver}"
