import pytest
from django.urls import reverse
from rest_framework.test import APIClient, APIRequestFactory
from rest_framework import status
from social_media_project.apps.post_service.models import User, Post, Comment


@pytest.mark.django_db
class TestBlogPostAPI:
    """
    Test suite for the Blog Post API endpoints.
    """

    def setup_method(self):
        """
        Setup method to initialize the test client, create a test user, a post, and a comment.
        This fixture runs before each test method.
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
        self.post = Post.objects.create(
            title="Test Post", content="Test content", user=self.user
        )
        self.comment = Comment.objects.create(
            post=self.post, content="Test comment", user=self.user
        )

    def test_list_posts(self):
        """
        Test listing all posts.
        """
        url = reverse("retrieve_all")
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert "data" in response.data
        assert response.data["message"] == "Post retrieved successfully"

    def test_create_post(self):
        """
        Test creating a new post.
        """
        url = reverse("create_post")
        data = {
            "title": "New Post",
            "content": "New content",
        }
        response = self.client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["message"] == "Post created successfully"

    def test_create_post_no_content(self):
        """
        Test creating a post with no content.
        """
        url = reverse("create_post")
        data = {
            "title": "New Post",
            "content": "",
        }
        response = self.client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_retrieve_post(self):
        """
        Test retrieving a single post.
        """
        url = reverse("retrieve", kwargs={"post_id": self.post.pk})
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"]["title"] == self.post.title

    def test_retrieve_post_not_exist(self):
        """
        Test retrieving a non-existent post.
        """
        url = reverse("retrieve", kwargs={"post_id": 999})
        response = self.client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["message"] == "Something went wrong"
        assert "errors" in response.data

    def test_update_post(self):
        """
        Test updating an existing post.
        """
        url = reverse("update_post", kwargs={"pk": self.post.pk})
        data = {
            "title": "Updated Post",
            "content": "Updated content",
        }
        response = self.client.put(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["message"] == "Post updated successfully"

    def test_update_post_not_owner(self):
        """
        Test updating a post by a user who is not the owner.
        """
        # Create a new user who is not the owner of the post
        other_user = User.objects.create_user(
            username="otheruser",
            password="otherpass",
            email="otheruser@example.com",
            is_active=True,
        )

        # Authenticate as the other user
        self.client.force_authenticate(user=other_user)

        url = reverse("update_post", kwargs={"pk": self.post.pk})
        data = {
            "title": "Updated Post by Other User",
            "content": "Updated content by other user",
        }
        response = self.client.put(url, data, format="json")

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["message"] == "You do not have ownership rights to edit this post."

        # Re-authenticate as the original user
        self.client.force_authenticate(user=self.user)

    def test_delete_post_not_owner(self):
        """
        Test deleting a post by a user who is not the owner.
        """
        # Create a new user who is not the owner of the post
        other_user = User.objects.create_user(
            username="otheruser",
            password="otherpass",
            email="otheruser@example.com",
            is_active=True,
        )

        # Authenticate as the other user
        self.client.force_authenticate(user=other_user)

        url = reverse("delete_post", kwargs={"pk": self.post.pk})
        response = self.client.delete(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["message"] == "You do not have ownership rights to delete this post."

        # Re-authenticate as the original user
        self.client.force_authenticate(user=self.user)


    def test_update_post_not_exist(self):
        """
        Test updating a non-existent post.
        """
        url = reverse("update_post", kwargs={"pk": 999})
        data = {
            "title": "Updated Post",
            "content": "Updated content",
        }
        response = self.client.put(url, data, format="json")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["message"] == "Something went wrong"
        assert "errors" in response.data

    def test_delete_post(self):
        """
        Test deleting an existing post.
        """
        url = reverse("delete_post", kwargs={"pk": self.post.pk})
        response = self.client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_post_not_exist(self):
        """
        Test deleting a non-existent post.
        """
        url = reverse("delete_post", kwargs={"pk": 999})
        response = self.client.delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["message"] == "Something went wrong"
        assert "errors" in response.data

    def test_update_post_invalid_data(self):
        """
        Test updating a post with invalid data to trigger the else statement.
        """
        url = reverse("update_post", kwargs={"pk": self.post.pk})
        data = {
            "title": "",
            "content": "Updated content",
        }
        response = self.client.put(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["message"] == "Something went wrong"
        assert "errors" in response.data
