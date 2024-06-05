import pytest
from django.urls import reverse
from rest_framework.test import APIClient, APIRequestFactory
from rest_framework import status
from social_media_project.apps.post_service.models import User, Post, Comment

@pytest.mark.django_db
class TestBlogPostAPI:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass',
            email='testuser@example.com',
            is_active=True
        )
        self.client.force_authenticate(user=self.user)
        self.factory = APIRequestFactory()
        self.post = Post.objects.create(title='Test Post', content='Test content', user=self.user)
        self.comment = Comment.objects.create(post=self.post, content='Test comment', user=self.user)

    def test_list_posts(self):
        url = reverse('retrieve_all')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'data' in response.data
        assert response.data['message'] == "Post retrieved successfully"

    def test_create_post(self):
        url = reverse('create_post')
        data = {
            'title': 'New Post',
            'content': 'New content',
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['message'] == "Post created successfully"



    def test_create_post_no_content(self):
        url = reverse('create_post')
        data = {
            'title': 'New Post',
            'content': '',
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_retrieve_post(self):
        url = reverse('retrieve', kwargs={'pk': self.post.pk})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['data']['title'] == self.post.title

    def test_retrieve_post_not_exist(self):
        url = reverse('retrieve', kwargs={'pk': 999})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['message'] == "Something went wrong"
        assert "errors" in response.data

    def test_update_post(self):
        url = reverse('update_post', kwargs={'pk': self.post.pk})
        data = {
            'title': 'Updated Post',
            'content': 'Updated content',
        }
        response = self.client.put(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['message'] == "Post updated successfully"

    def test_update_post_not_exist(self):
        url = reverse('update_post', kwargs={'pk': 999})
        data = {
            'title': 'Updated Post',
            'content': 'Updated content',
        }
        response = self.client.put(url, data, format='json')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['message'] == "Something went wrong"
        assert "errors" in response.data

    def test_delete_post(self):
        url = reverse('delete_post', kwargs={'pk': self.post.pk})
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_post_not_exist(self):
        url = reverse('delete_post', kwargs={'pk': 999})
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['message'] == "Something went wrong"
        assert "errors" in response.data
