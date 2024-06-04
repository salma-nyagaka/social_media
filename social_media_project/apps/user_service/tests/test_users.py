# user_service/tests/test_user_views.py

import pytest
from django.urls import reverse
from django.test import TestCase
from unittest.mock import patch
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from social_media_project.apps.user_service.models import User
from social_media_project.apps.user_service.serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    UserLoginAPIViewSerializer,
)


@pytest.mark.django_db
class TestUserAPI(TestCase):
    """
    Test suite for the User API.
    """

    def setUp(self):
        """
        Set up test environment.
        Creates a test user and authenticates the API client.
        """
        self.user = User.objects.create_user(
            username="testuser", password="testpassword", email="test@example.com"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list_users(self):
        """
        Test listing all users.
        """
        url = reverse("list_users")
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["data"]) == User.objects.count()

    @patch("social_media_project.apps.notification_service.tasks.send_email_task.delay")
    def test_create_user(self, mock_send_email_task):
        """
        Test creating a new user.
        """
        self.client.logout()
        url = reverse("create_user")
        data = {
            "username": "newuser",
            "password": "newpassword",
            "email": "newuser@example.com",
        }
        response = self.client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.count() == 2
        new_user = User.objects.get(username="newuser")
        assert new_user.email == "newuser@example.com"

    def test_retrieve_user(self):
        """
        Test retrieving a user.
        """
        url = reverse("retrieve_user", args=[self.user.id])
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"]["username"] == self.user.username

    def test_update_user(self):
        """
        Test updating a user.
        """
        url = reverse("update_user", args=[self.user.id])
        data = {"username": "updateduser"}
        response = self.client.patch(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        self.user.refresh_from_db()
        assert self.user.username == "updateduser"

    # def test_partial_update_user(self):
    #     """
    #     Test partially updating a user.
    #     """
    #     url = reverse('user-detail', args=[self.user.id])  # Update this to the correct name for your user partial update view
    #     data = {
    #         'username': 'partiallyupdateduser'
    #     }
    #     response = self.client.patch(url, data, format='json')

    #     assert response.status_code == status.HTTP_200_OK
    #     self.user.refresh_from_db()
    #     assert self.user.username == 'partiallyupdateduser'

    def test_delete_user(self):
        """
        Test deleting a user.
        """
        url = reverse(
            "delete_user", args=[self.user.id]
        )  # Update this to the correct name for your user delete view
        response = self.client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert User.objects.count() == 0

    def test_me_endpoint(self):
        """
        Test retrieving the current authenticated user.
        """
        url = reverse(
            "get_current_user"
        )  # Update this to the correct name for your user "me" endpoint
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["username"] == self.user.username

    @patch("jwt.decode")
    def test_activate_account(self, mock_jwt_decode):
        """
        Test activating a user account.
        """
        mock_jwt_decode.return_value = {
            "user_id": self.user.id,
            "exp": (timezone.now() + timezone.timedelta(days=1)).timestamp(),
        }
        token = "fake-jwt-token"
        url = reverse("activate_account", args=[token])

        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        self.user.refresh_from_db()
        assert self.user.is_active
