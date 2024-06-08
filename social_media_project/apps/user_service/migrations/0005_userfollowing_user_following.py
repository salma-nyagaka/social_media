# Generated by Django 5.0.6 on 2024-06-05 13:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user_service", "0004_alter_user_first_name_alter_user_last_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserFollowing",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "following_user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_following_id",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="following_user_id",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="user",
            name="following",
            field=models.ManyToManyField(
                related_name="followers",
                through="user_service.UserFollowing",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]