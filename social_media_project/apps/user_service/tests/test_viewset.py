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
    """
    Test suite for the UserViewSet.
    """

    def setUp(self):
        """
        Setup method to initialize the test client, create a test user, and authenticate the user.
        This method runs before each test method.
        """
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
        """
        Test get_serializer_class method for the 'create' action.
        """
        view = UserViewSet()
        view.action = "create"
        view.request = self.factory.post(reverse("create_user"))
        serializer_class = view.get_serializer_class()

        assert serializer_class == UserCreateSerializer

    def test_get_serializer_class_update(self):
        """
        Test get_serializer_class method for the 'update' action.
        """
        view = UserViewSet()
        view.action = "update"
        view.request = self.factory.put(reverse("update_user", args=[self.user.pk]))
        serializer_class = view.get_serializer_class()

        assert serializer_class == UserUpdateSerializer

    def test_get_serializer_class_partial_update(self):
        """
        Test get_serializer_class method for the 'partial_update' action.
        """
        view = UserViewSet()
        view.action = "partial_update"
        view.request = self.factory.patch(reverse("update_user", args=[self.user.pk]))
        serializer_class = view.get_serializer_class()

        assert serializer_class == UserUpdateSerializer

    def test_get_serializer_class_default(self):
        """
        Test get_serializer_class method for the default action.
        """
        view = UserViewSet()
        view.action = "list"
        view.request = self.factory.get(reverse("list_users"))
        serializer_class = view.get_serializer_class()

        assert serializer_class == UserSerializer
