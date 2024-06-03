# post_service/tests/test_views.py
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from social_media_project.apps.user_service.models import User
from social_media_project.apps.post_service.models import Post, Comment
from rest_framework_simplejwt.tokens import RefreshToken
from django.test import TestCase

@pytest.mark.django_db
class TestPostAPI(TestCase):
    """Test suite for Post and Comment APIs."""

    def setUp(self):
        """Set up test data and API client."""
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        # Obtain the JWT token
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        self.post = Post.objects.create(user=self.user, content='Test post content')

    def test_create_post(self):
        """Test creating a new post."""
        url = reverse('post-list')
        data = {'content': 'Test post'}
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Post.objects.count() == 2  # including the setup post
        assert Post.objects.filter(content='Test post').exists()

    def test_get_posts(self):
        """Test retrieving a list of posts."""
        url = reverse('post-list')
        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['content'] == 'Test post content'


    def test_add_and_get_comments(self):
        """Test retrieving comments for a post."""
        Comment.objects.create(post=self.post, user=self.post.user, content='Test comment')
        url = reverse('post-detail', kwargs={'pk': self.post.pk})
        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['comments']) == 1
        assert response.data['comments'][0]['content'] == 'Test comment'
