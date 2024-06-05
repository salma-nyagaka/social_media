import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from unittest.mock import patch
from social_media_project.apps.user_service.models import User
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient, APITestCase, APIRequestFactory
from datetime import datetime, timedelta

from social_media_project.apps.user_service.views import UserViewSet
from social_media_project.apps.user_service.serializers import (
    UserCreateSerializer,
    UserUpdateSerializer,
)


@pytest.mark.django_db
class TestUserAPI:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass",
            email="testuser@example.com",
            first_name="test1",
            last_name="test2",
            is_active=True,
        )
        self.client.force_authenticate(user=self.user)
        self.user_url = reverse("retrieve_user", kwargs={"pk": self.user.pk})
        self.login_url = reverse("user_login")

        self.factory = APIRequestFactory()

    def test_create_user(self):
        url = reverse("create_user")
        data = {
            "username": "newuser",
            "password": "newpass",
            "email": "newuser@example.com",
            "first_name": "test1",
            "last_name": "test2",
        }
        response = self.client.post(url, data, format="json")
        assert response.status_code == 201
        assert (
            response.data["message"]
            == "Your account has been successfully created. Please activate your account by clicking the link sent to your email."
        )

    def test_list_users(self):
        url = reverse("list_users")
        response = self.client.get(url)
        assert response.status_code == 200
        assert "data" in response.data
        assert len(response.data["data"]) > 0

    def test_retrieve_user(self):
        response = self.client.get(self.user_url)
        assert response.status_code == 200
        assert response.data["data"]["username"] == self.user.username

    def test_retrieve_user_not_exist(self):
        url = reverse("retrieve_user", args=[999])
        response = self.client.get(url, format="json")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["message"] == "Something went wrong"
        assert response.data["error"] == "The user does not exist"

    def test_update_user(self):
        url = reverse("update_user", kwargs={"pk": self.user.pk})
        data = {"email": "updatedemail@example.com"}
        response = self.client.patch(url, data, format="json")
        assert response.status_code == 200
        assert response.data["data"]["email"] == "updatedemail@example.com"

    def test_nonexistant_update_user(self):
        non_existent_pk = 999
        url = reverse("update_user", kwargs={"pk": non_existent_pk})
        data = {"email": "updatedemail@example.com"}
        response = self.client.patch(url, data, format="json")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["message"] == "Something went wrong"
        assert response.data["error"] == "User does not exist"

    def test_delete_user(self):
        url = reverse("delete_user", kwargs={"pk": self.user.pk})
        response = self.client.delete(url)
        assert response.status_code == 204

    def test_delete_user_not_exist(self):
        non_existent_pk = 999
        url = reverse("delete_user", kwargs={"pk": non_existent_pk})
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["message"] == "Something went wrong"
        assert response.data["error"] == "The user does not exist"

    def test_user_login_success(self):
        data = {"username": "testuser", "password": "testpass"}
        response = self.client.post(self.login_url, data, format="json")
        assert response.status_code == 200
        assert "token" in response.data["data"]

    def test_user_login_invalid_credentials(self):
        data = {"username": "testuser", "password": "wrongpass"}
        response = self.client.post(self.login_url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_current_user(self):
        """
        Test retrieving the current authenticated user.
        """
        url = reverse("get_current_user")
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK

    @patch("jwt.decode")
    def test_activate_account_success(self, mock_jwt_decode):
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
