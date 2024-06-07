import pytest
from django.urls import reverse
from rest_framework.test import APIClient, APIRequestFactory
from rest_framework import status
from social_media_project.apps.user_service.models import User, UserFollowing


@pytest.mark.django_db
class TestFollowUnfollowAPI:
    """
    Test suite for the Follow, Unfollow, and Followers API endpoints.
    """

    def setup_method(self):
        """
        Setup method to initialize the test client and create test users.
        This fixture runs before each test method.
        """
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            username="testuser1",
            password="testpass1",
            email="testuser1@example.com",
            is_active=True,
        )
        self.user2 = User.objects.create_user(
            username="testuser2",
            password="testpass2",
            email="testuser2@example.com",
            is_active=True,
        )
        self.client.force_authenticate(user=self.user1)
        self.factory = APIRequestFactory()

    def test_follow_user(self):
        """
        Test following another user.
        """
        url = reverse("follow", kwargs={"pk": self.user2.pk})
        response = self.client.post(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["message"] == f"You have successfully followed {self.user2.username}"
        assert UserFollowing.objects.filter(user_id=self.user1, following_user_id=self.user2).exists()

    def test_follow_user_yourself(self):
        """
        Test trying to follow yourself.
        """
        url = reverse("follow", kwargs={"pk": self.user1.pk})
        response = self.client.post(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["status"] == "You cannot follow yourself"

    def test_follow_user_already_following(self):
        """
        Test trying to follow a user you are already following.
        """
        UserFollowing.objects.create(user_id=self.user1, following_user_id=self.user2)
        url = reverse("follow", kwargs={"pk": self.user2.pk})
        response = self.client.post(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["status"] == "You are already following this user"

    def test_unfollow_user(self):
        """
        Test unfollowing a user you are following.
        """
        UserFollowing.objects.create(user_id=self.user1, following_user_id=self.user2)
        url = reverse("unfollow", kwargs={"pk": self.user2.pk})
        response = self.client.post(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["message"] == f"You have successfully unfollowed {self.user2.username}"
        assert not UserFollowing.objects.filter(user_id=self.user1, following_user_id=self.user2).exists()

    def test_unfollow_user_yourself(self):
        """
        Test trying to unfollow yourself.
        """
        url = reverse("unfollow", kwargs={"pk": self.user1.pk})
        response = self.client.post(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["status"] == "You cannot unfollow yourself"

    def test_unfollow_user_not_following(self):
        """
        Test trying to unfollow a user you are not following.
        """
        url = reverse("unfollow", kwargs={"pk": self.user2.pk})
        response = self.client.post(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["status"] == "You are not following this user"

    def test_list_followers(self):
        """
        Test listing all followers of a user.
        """
        UserFollowing.objects.create(user_id=self.user2, following_user_id=self.user1)
        url = reverse("followers", kwargs={"pk": self.user1.pk})
        response = self.client.get(url)
