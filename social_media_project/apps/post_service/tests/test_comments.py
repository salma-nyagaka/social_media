import pytest
from django.urls import reverse
from rest_framework.test import APIClient, APIRequestFactory
from rest_framework import status
from unittest.mock import patch
from social_media_project.apps.post_service.models import User, Post, Comment


@pytest.mark.django_db
class TestCommentAPI:
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

    def test_list_comments(self):
        url = reverse('list_comments')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'data' in response.data
        assert response.data['message'] == "Comments retrieved successfully"

    def test_create_comment(self):
        url = reverse('create_comment')
        data = {
            'post': self.post.pk,
            'content': 'New comment',
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['message'] == "Comment created successfully"
        
    
    def test_create_comment_no_content(self):
        url = reverse('create_comment')
        data = {
            'post': self.post.pk,
            'content': '',
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_retrieve_comment(self):
        url = reverse('retrieve_comment', kwargs={'pk': self.comment.pk})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['data']['content'] == self.comment.content

    def test_retrieve_comment_not_exist(self):
        url = reverse('retrieve_comment', kwargs={'pk': 999})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_comment(self):
        url = reverse('update_comment', kwargs={'pk': self.comment.pk})
        data = {
            'post': self.post.id,
            'content': 'Updated comment',
        }
        response = self.client.put(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['message'] == "Comment updated successfully"

    def test_update_comment_not_exist(self):
        url = reverse('update_comment', kwargs={'pk': 999})
        data = {
            'content': 'Updated comment',
        }
        response = self.client.put(url, data, format='json')
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_update_comment_no_content(self):
        url = reverse('update_comment', kwargs={'pk': 999})
        data = {
            'content': '',
        }
        response = self.client.put(url, data, format='json')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        

    def test_delete_comment(self):
        url = reverse('delete_comment', kwargs={'pk': self.comment.pk})
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_comment_not_exist(self):
        url = reverse('delete_comment', kwargs={'pk': 999})
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
    
    @patch('social_media_project.apps.post_service.serializers.CommentSerializer.save', side_effect=Exception('Test exception'))
    def test_create_comment_exception(self, mock_save):
        """
        Test the exception handling in the perform_create method.
        """
        url = reverse('create_comment')
        data = {
            'post': self.post.pk,
            'content': 'New comment',
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['message'] == "Something went wrong"
        assert 'detail' in response.data['errors']
        assert response.data['errors']['detail'] == 'Test exception'
