from __future__ import absolute_import, unicode_literals
import os
import time
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "social_media_project.settings")


def create_celery_app():
    while True:
        try:
            app = Celery("social_media_project")
            app.config_from_object("django.conf:settings", namespace="CELERY")
            app.autodiscover_tasks()
            return app
        except Exception as e:
            print(f"Retrying to connect to broker in 5 seconds... Error: {e}")
            time.sleep(5)


app = create_celery_app()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
