# Generated by Django 5.0.6 on 2024-06-03 16:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("post_service", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="user",
        ),
    ]