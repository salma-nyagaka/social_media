import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from social_media_project.apps.user_service.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status

@pytest.fixture
def api_client():
    return APIClient()

# @pytest.mark.django_db
def generate_token():
    client = APIClient()
    user = User.objects.get_or_create(username='testuser', email='test@example.com', password='testpassword', is_active=True)
    url = reverse('user_login')  # Assuming 'user-login' is the name of your login endpoint

    # Valid login credentials
    data = {'username': 'testuser', 'password': 'testpassword'}
    response = client.post(url, data, format='json')
    
    import pdb
    pdb.set_trace()

    return response

# @pytest.mark.django_db  # Use the django_db fixture for database access
# def test_user_login():
#     # client = APIClient()
#     # user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword', is_active=True)
#     # url = reverse('user_login')  # Assuming 'user-login' is the name of your login endpoint

#     # # Valid login credentials
#     # data = {'username': 'testuser', 'password': 'testpassword'}
#     # response = client.post(url, data, format='json')
#     generate_token()
#     # import pdb
#     # pdb.set_trace()
#     assert response.status_code == status.HTTP_200_OK, "You have successfully logged in"

#     # Invalid login credentials
#     data = {'username': 'invalid_username', 'password': 'invalid_password'}
#     response = client.post(url, data, format='json')
#     assert response.status_code == status.HTTP_400_BAD_REQUEST, "Login should fail"


@pytest.fixture
def create_user():
    user = User.objects.create(username='testuser', email='test@example.com')
    user.set_password('testpassword')
    user.save()
    return user

@pytest.mark.django_db  # Use the django_db fixture for database access
def test_user_create(api_client):
    url = reverse('create_user')  # Make sure 'user-create' is the correct view name
    data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword'
    }
    response = api_client.post(url, data)
    assert response.status_code == 201
    
    

# def generate_token():
#     # client = APIClient()
#     # user = User.objects.get_or_create(username='testuser', email='test@example.com', password='testpassword', is_active=True)
#     url = reverse('user_login')  # Assuming 'user-login' is the name of your login endpoint

#     # Valid login credentials
#     data = {'username': 'testuser', 'password': 'testpassword'}
#     response = api_client.post(url, data)
    
#     import pdb
#     pdb.set_trace()

#     return response

# generate_token()


