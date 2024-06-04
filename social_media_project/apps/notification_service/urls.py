# notification_service/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet, test_email,test_kafka_notification

router = DefaultRouter()
router.register(r'notifications', NotificationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('test-email/', test_email, name='test_email'),
    path('test-kafka-notification/', test_kafka_notification, name='test_kafka_notification'),

]
