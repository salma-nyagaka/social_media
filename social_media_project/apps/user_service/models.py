from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_active = models.EmailField(default=False)
    # activation_expiry = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
