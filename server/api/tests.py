from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import User, Order, Address, Subscription
from .serializers import *

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
    

class AddressCreateViewTest(APITestCase):
    def setUp(self):
        url = reverse('user-register')
        data = {
            'email': 'firatkizilboga@gmail.com',
            'first_name': 'Firat',
            'last_name': 'Kizilboga',
            'password': 'Aa125423',
        }
        response = self.client.post(url, data, format='json')
        self.data = data

        url = reverse('user-login')
        email = self.data['email']
        password = self.data['password']
        response = self.client.post(url, {'email': email, 'password':password}, format='json')
        self.token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
    
    def test_create_address(self):
        url = reverse('address-create')
        data = {
            'title': 'Home',
            'address_line1': 'Kadikoy',
            'address_line2': 'Istanbul',
            'city': 'Istanbul',
            'country': 'Turkey',
            'postal_code': '34732',
        }
        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_address_with_no_title(self):
        url = reverse('address-create')
        data = {
            'address_line1': 'Kadikoy',
            'address_line2': 'Istanbul',
            'city': 'Istanbul',
            'country': 'Turkey',
            'postal_code': '34732',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_address_with_no_address_line1(self):
        url = reverse('address-create')
        data = {
            'title': 'Home',
            'address_line2': 'Istanbul',
            'city': 'Istanbul',
            'country': 'Turkey',
            'postal_code': '34732',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_address_with_no_city(self):
        url = reverse('address-create')
        data = {
            'title': 'Home',
            'address_line1': 'Kadikoy',
            'address_line2': 'Istanbul',
            'country': 'Turkey',
            'postal_code': '34732',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    
    def test_create_address_unauthenticated(self):
        url = reverse('address-create')
        data = {
            'title': 'Home',
            'address_line1': 'Kadikoy',
            'address_line2': 'Istanbul',
            'city': 'Istanbul',
            'country': 'Turkey',
            'postal_code': '34732',
        }
        client = APIClient()
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class AddressListViewTest(APITestCase):
    def setUp(self):
        url = reverse('user-register')
        data = {
            'email': 'firatkizilboga@gmail.com',
            'first_name': 'Firat',
            'last_name': 'Kizilboga',
            'password': 'Aa125423',
        }
        response = self.client.post(url, data, format='json')
        self.data = data

        url = reverse('user-login')
        email = self.data['email']
        password = self.data['password']
        response = self.client.post(url, {'email': email, 'password':password}, format='json')
        self.token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        url = reverse('address-create')
        data = {
            'title': 'Home',
            'address_line1': 'Kadikoy',
            'address_line2': 'Istanbul',

            'city': 'Istanbul',
            'country': 'Turkey',
            'postal_code': '34732',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('address-create')
        data = {
            'title': 'Work',
            'address_line1': 'Kadikoy',
            'address_line2': 'Istanbul',
            'city': 'Istanbul',
            'country': 'Turkey',
            'postal_code': '34732',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_list_addresses(self):
        url = reverse('address-list')
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_addresses_unauthenticated(self):
        url = reverse('address-list')
        client = APIClient()
        response = client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_addresses_with_different_account(self):
        url = reverse('user-register')
        data = {
            'email': 'firat2@email.com',
            'first_name': 'Firat',
            'last_name': 'Kizilboga',
            'password': 'Aa125423',
        }
        self.client = APIClient()
        response = self.client.post(url, data, format='json')
        url = reverse('user-login')
        email = data['email']
        password = data['password']
        response = self.client.post(url, {'email': email, 'password':password}, format='json')
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        #add 1 address
        url = reverse('address-create')
        data = {
            'title': 'Home',
            'address_line1': 'Kadikoy',
            'address_line2': 'Istanbul',
            'city': 'Istanbul',
            'country': 'Turkey',
            'postal_code': '34732',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #list addresses
        url = reverse('address-list')
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class AddressDetailViewTest(APITestCase):
    def setUp(self):
        url = reverse('user-register')
        data = {
            'email': 'firatkizilboga@gmail.com',
            'first_name': 'Firat',
            'last_name': 'Kizilboga',
            'password': 'Aa125423',
        }
        response = self.client.post(url, data, format='json')
        self.data = data

        url = reverse('user-login')
        email = self.data['email']
        password = self.data['password']
        response = self.client.post(url, {'email': email, 'password':password}, format='json')
        self.token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        url = reverse('address-create')
        data = {
            'title': 'Home',
            'address_line1': 'Kadikoy',
            'address_line2': 'Istanbul',

            'city': 'Istanbul',
            'country': 'Turkey',
            'postal_code': '34732',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('address-create')
        data = {
            'title': 'Work',
            'address_line1': 'Kadikoy',
            'address_line2': 'Istanbul',
            'city': 'Istanbul',
            'country': 'Turkey',
            'postal_code': '34732',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_address(self):
        url = reverse('address-list')
        response = self.client.post(url, format='json')
        print(response.data)
        address_id = response.data[0]['id']
        url = reverse('address-detail', args=[address_id])
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], address_id)

    def test_retrieve_address_unauthenticated(self):
        url = reverse('address-list')
        response = self.client.post(url, format='json')
        address_id = response.data[0]['id']
        url = reverse('address-detail', args=[address_id])
        client = APIClient()
        response = client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_retrieve_address_with_different_account(self):
        url = reverse('user-register')
        data = {
            'email': 'firatkizilboga222@gmail.com',
            'first_name': 'Firat',
            'last_name': 'Kizilboga',
            'password': 'Aa125423',
        }
        self.client = APIClient()
        response = self.client.post(url, data, format='json')
        url = reverse('user-login')
        email = data['email']
        password = data['password']
        response = self.client.post(url, {'email': email, 'password':password}, format='json')
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        url = reverse('address-detail', args=["0"])
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    

class AddressDeleteViewTest(APITestCase):
    def setUp(self):
        url = reverse('user-register')
        data = {
            'email': 'firatkizilboga@gmail.com',
            'first_name': 'Firat',
            'last_name': 'Kizilboga',
            'password': 'Aa125423',
        }
        response = self.client.post(url, data, format='json')
        self.data = data

        url = reverse('user-login')
        email = self.data['email']
        password = self.data['password']
        response = self.client.post(url, {'email': email, 'password':password}, format='json')

        self.token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        url = reverse('address-create')
        data = {
            'title': 'Home',
            'address_line1': 'Kadikoy',
            'address_line2': 'Istanbul',
            'city': 'Istanbul',
            'country': 'Turkey',
            'postal_code': '34732',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_delete_address(self):
        url = reverse('address-list')
        response = self.client.post(url, format='json')
        address_id = response.data[0]['id']
        url = reverse('address-delete', args=[address_id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
