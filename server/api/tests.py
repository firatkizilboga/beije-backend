from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import User, Order, Address, Subscription
from .serializers import UserSerializer #,OrderSerializer, AddressSerializer, SubscriptionSerializer

# Create your tests here.

class UserCreateViewTest(APITestCase):
    def test_create_user(self):
        url = reverse('user-register')
        print(url)

        data = {
            'email': 'firatkizilboga11@gmail.com',
            'first_name': 'Firat',
            'last_name': 'Kizilboga',
            'password': 'Aa125423',
        }
        self.client = APIClient()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return data

    def test_create_user_with_small_password(self):
        url = reverse('user-register')
        data = {
            'email': 'firatkizilboga12@gmail.com',
            'first_name': 'Firat',
            'last_name': 'Kizilboga',
            'password': 'Aa125',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_no_password(self):
        url = reverse('user-register')
        data = {
            'email': 'firatkizilboga123@gmail.com',
            'first_name': 'Firat',
            'last_name': 'Kizilboga',
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    
    
class UserLoginViewTest(APITestCase):
    def setUp(self):
        url = reverse('user-register')
        data = {
            'email': 'firatkizilboga11@gmail.com',
            'first_name': 'Firat',
            'last_name': 'Kizilboga',
            'password': 'Aa125423',
        }
        self.client = APIClient()
        response = self.client.post(url, data, format='json')
        self.data = data


    def test_login_user(self):
        email = self.data['email']
        password = self.data['password']
        url = reverse('user-login')
        print(url)
        response = self.client.post(url, {'email': email, 'password':password}, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_user_with_wrong_password(self):
        url = reverse('user-login')
        email = self.data['email']

        response = self.client.post(url, {'email': email, 'password':'wrong-password'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


