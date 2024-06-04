# user_service/tests/test_user_views.py

import pytest
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from social_media_project.apps.user_service.models import User



@pytest.mark.django_db
class TestUserLoginAPIView(TestCase):
    """
    Test suite for the UserLoginAPIView.
    """
    
    def setUp(self):
        """
        Set up test environment.
        Creates a test user and API client.
        """
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='test@example.com')
        self.client = APIClient()
    
    def test_login_wrong_credentials(self):
        """
        Test user login with wrong credentials.
        """
        url = reverse('user_login')  # Ensure this matches your URL name for login
        data = {
            'email': 'test@example.com',
            'password': 'testpasswsord'
        }
        response = self.client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'token' in response.data
        
    def test_login_with_no_password(self):
        """
        Test user login with wrong credentials.
        """
        url = reverse('user_login')  # Ensure this matches your URL name for login
        data = {
            'username': 'test@example.com',
            'password': ''
        }
        response = self.client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'Password is required' in response.data