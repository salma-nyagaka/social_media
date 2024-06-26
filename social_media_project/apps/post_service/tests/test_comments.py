import pytest
from django.urls import reverse
from rest_framework.test import APIClient, APIRequestFactory
from rest_framework import status
from unittest.mock import patch
from social_media_project.apps.post_service.models import User, Post, Comment


@pytest.mark.django_db
class TestCommentAPI:
    """
    Test suite for the Comment API endpoints.
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
        self.user2 = User.objects.create_user(
            username="otheruser",
            password="testpass",
            email="otheruser@example.com",
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

    def test_list_comments(self):
        """
        Test listing all comments.
        """
        url = reverse("list_comments")
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert "data" in response.data
        assert response.data["message"] == "Comments retrieved successfully"

    def test_create_comment(self):
        """
        Test creating a new comment.
        """
        url = reverse("create_comment")
        data = {
            "post": self.post.pk,
            "content": "New comment",
        }
        response = self.client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["message"] == "Comment created successfully"

    def test_create_comment_no_content(self):
        """
        Test creating a comment with no content.
        """
        url = reverse("create_comment")
        data = {
            "post": self.post.pk,
            "content": "",
        }
        response = self.client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_retrieve_comment(self):
        """
        Test retrieving a single comment.
        """
        url = reverse("retrieve_comment", kwargs={"pk": self.comment.pk})
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"]["content"] == self.comment.content

    def test_retrieve_comment_not_exist(self):
        """
        Test retrieving a non-existent comment.
        """
        url = reverse("retrieve_comment", kwargs={"pk": 999})
        response = self.client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_comment(self):
        """
        Test updating an existing comment.
        """
        url = reverse("update_comment", kwargs={"comment_id": self.comment.pk})
        data = {
            "post": self.post.id,
            "content": "Updated comment",
        }
        response = self.client.put(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["message"] == "Comment updated successfully"

    def test_update_comment_not_exist(self):
        """
        Test updating a non-existent comment.
        """
        url = reverse("update_comment", kwargs={"comment_id": 999})
        data = {
            "content": "Updated comment",
        }
        response = self.client.put(url, data, format="json")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_comment_no_content(self):
        """
        Test updating a comment with no content.
        """
        url = reverse("update_comment", kwargs={"comment_id": self.comment.pk})
        data = {
            "content": "",
        }
        response = self.client.put(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_delete_comment(self):
        """
        Test deleting an existing comment.
        """
        url = reverse("delete_comment", kwargs={"comment_id": self.comment.pk})
        response = self.client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_comment_not_exist(self):
        """
        Test deleting a non-existent comment.
        """
        url = reverse("delete_comment", kwargs={"comment_id": 999})
        response = self.client.delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @patch(
        "social_media_project.apps.post_service.serializers.CommentSerializer.save",
        side_effect=Exception("Test exception"),
    )
    def test_create_comment_exception(self, mock_save):
        """
        Test handling exceptions in the comment creation process.
        """
        url = reverse("create_comment")
        data = {
            "post": self.post.pk,
            "content": "New comment",
        }
        response = self.client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["message"] == "Something went wrong"
        assert "detail" in response.data["errors"]
        assert response.data["errors"]["detail"] == "Test exception"

    def test_delete_comment_no_permission(self):
            """
            Test that a user cannot update another user's comment.
            """
            self.client.force_authenticate(user=self.user2)
            url = reverse("delete_comment", kwargs={"comment_id": self.comment.pk})
            data = {
                "content": "Delete comment by another user",
            }
            response = self.client.delete(url, data, format="json")


            assert response.status_code == status.HTTP_403_FORBIDDEN
            assert response.data == {'message': 'You do not have ownership rights to delete this comment'}
            
    def test_update_comment_no_permission(self):
        """
        Test that a user cannot update another user's comment.
        """
        self.client.force_authenticate(user=self.user2)
        url = reverse("update_comment", kwargs={"comment_id": self.comment.pk})
        data = {
            "content": "Updated comment by another user",
        }
        response = self.client.put(url, data, format="json")


        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data == {'message': 'You do not have ownership rights to update this comment'}