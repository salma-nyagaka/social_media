import pytest
from rest_framework.test import APIClient, APITestCase, APIRequestFactory
from django.urls import reverse
from social_media_project.apps.user_service.views import UserViewSet
from social_media_project.apps.user_service.serializers import (
    UserCreateSerializer,
    UserUpdateSerializer,
    UserSerializer,
)
from social_media_project.apps.user_service.models import User
from rest_framework import status


@pytest.mark.django_db
class TestUserViewSet(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass",
            email="testuser@example.com",
            is_active=True,
        )
        self.client.force_authenticate(user=self.user)
        self.factory = APIRequestFactory()

    def test_get_serializer_class_create(self):
        view = UserViewSet.as_view(actions={"post": "create"})
        request = self.factory.post(reverse("create_user"))
        view = UserViewSet()
        view.action = "create"
        view.request = request
        serializer_class = view.get_serializer_class()
        assert serializer_class == UserCreateSerializer

    def test_get_serializer_class_update(self):
        view = UserViewSet.as_view(actions={"put": "update"})
        request = self.factory.put(reverse("update_user", args=[self.user.pk]))
        view = UserViewSet()
        view.action = "update"
        view.request = request
        serializer_class = view.get_serializer_class()
        assert serializer_class == UserUpdateSerializer

    def test_get_serializer_class_partial_update(self):
        view = UserViewSet.as_view(actions={"patch": "partial_update"})
        request = self.factory.patch(reverse("update_user", args=[self.user.pk]))
        view = UserViewSet()
        view.action = "partial_update"
        view.request = request
        serializer_class = view.get_serializer_class()
        assert serializer_class == UserUpdateSerializer

    def test_get_serializer_class_default(self):
        view = UserViewSet.as_view(actions={"get": "list"})
        request = self.factory.get(reverse("list_users"))
        view = UserViewSet()
        view.action = "list"
        view.request = request
        serializer_class = view.get_serializer_class()
        assert serializer_class == UserSerializer
