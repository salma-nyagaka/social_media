# post_service/tests/test_views.py
"""
Test cases for BlogPost and Comment APIs.
"""

import pytest
from django.urls import reverse
from django.test import TestCase
from unittest.mock import patch
from rest_framework.test import APIClient
from social_media_project.apps.post_service.models import Post, Comment
from social_media_project.apps.user_service.models import User


@pytest.mark.django_db
class TestPostAPI(TestCase):
    """
    Test suite for the BlogPost and Comment APIs.
    """

    def setUp(self):
        """
        Set up test environment.
        Creates a test user and authenticates the API client.
        Also creates a test post.
        """
        self.user = User.objects.create_user(
            username="testuser", password="testpassword", email="test@example.com"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.post = Post.objects.create(
            title="Test Post", content="This is a test post", user=self.user
        )

    @patch("social_media_project.apps.notification_service.tasks.send_email_task.delay")
    def test_create_post(self, mock_send_email_task):
        """
        Test creating a new blog post.
        Verifies that the post is created and an email notification is sent.
        """
        url = reverse(
            "post-list"
        )  # Update this to the correct name for your post list view
        data = {"title": "New Post", "content": "This is a new post"}
        response = self.client.post(url, data, format="json")

        assert response.status_code == 201
        assert Post.objects.count() == 2
        post = Post.objects.last()
        assert post.title == "New Post"

        # Check if the email task was called
        mock_send_email_task.assert_called_once()
        call_args = mock_send_email_task.call_args[1]
        assert call_args["subject"] == "New Post Created"
        assert 'A new post titled "New Post" has been created.' in call_args["message"]

    @patch("social_media_project.apps.notification_service.tasks.send_email_task.delay")
    def test_create_comment(self, mock_send_email_task):
        """
        Test creating a new comment on a post.
        Verifies that the comment is created and an email notification is sent.
        """
        url = reverse(
            "comment-list"
        )  # Update this to the correct name for your comment list view
        data = {"post": self.post.id, "content": "This is a comment"}
        response = self.client.post(url, data, format="json")

        assert response.status_code == 201
        assert Comment.objects.count() == 1
        comment = Comment.objects.first()
        assert comment.content == "This is a comment"

        # Check if the email task was called
        mock_send_email_task.assert_called_once()
        call_args = mock_send_email_task.call_args[1]
        assert (
            call_args["subject"] == "New comment has been added to the post: Test Post"
        )
        assert "This is a comment" in call_args["message"]
