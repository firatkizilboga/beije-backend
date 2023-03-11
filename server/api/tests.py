from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import User, Order, Address, Subscription
from .serializers import *

# Create your tests here.
class BaseTest(APITestCase):
    def setUp(self):
        data = {
            'email': 'firatkizilboga11@gmail.com',
            'first_name': 'Firat',
            'last_name': 'Kizilboga',
            'password': 'Aa125423',
        }
        self.create_user(data)
        self.login_user(data['email'], data['password'])
    def create_user(self, data):
        url = reverse('user-register')
        self.client = APIClient()
        response = self.client.post(url, data, format='json')
        return response

    def login_user(self, email, password):
        url = reverse('user-login')
        response = self.client.post(url, {'email': email, 'password': password}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + response.data['token'])
        return response.data['token']

    def create_address(self, data):
        url = reverse('address-create')
        response = self.client.post(url, data, format='json')
        return response
    

    
    
    
class UserCreateViewTest(BaseTest):
    def setUp(self):
        pass
    def test_create_user(self):
        data = {
            'email': 'firatkizilboga11@gmail.com',
            'first_name': 'Firat',
            'last_name': 'Kizilboga',
            'password': 'Aa125423',
        }
        response = self.create_user(data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return data

    def test_create_user_with_small_password(self):
        data = {
            'email': 'firatkizilboga12@gmail.com',
            'first_name': 'Firat',
            'last_name': 'Kizilboga',
            'password': 'Aa125',
        }
        response = self.create_user(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_no_password(self):
        data = {
            'email': 'firatkizilboga123@gmail.com',
            'first_name': 'Firat',
            'last_name': 'Kizilboga',
        }
        response = self.create_user(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UserLoginViewTest(BaseTest):
    def setUp(self):
        data = {
            'email': 'firatkizilboga11@gmail.com',
            'first_name': 'Firat',
            'last_name': 'Kizilboga',
            'password': 'Aa125423',
        }
        response = self.create_user(data)
        self.token = self.login_user(data['email'], data['password'])

    def test_login_user(self):
        url = reverse('user-login')
        email = 'firatkizilboga11@gmail.com'
        password = 'Aa125423'
        response = self.client.post(url, {'email': email, 'password':password}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_user_with_wrong_password(self):
        url = reverse('user-login')
        email = 'firatkizilboga11@gmail.com'
        response = self.client.post(url, {'email': email, 'password':'wrong-password'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    

class AddressCreateViewTest(BaseTest):
    def setUp(self):
        super().setUp()

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
        response = self.create_address(data)
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
        response = self.create_address(data)
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
        response = self.create_address(data)
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
        response = self.create_address(data)
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
        self.client = APIClient()
        response = self.create_address(data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class AddressListViewTest(BaseTest):
    def setUp(self):
        super().setUp()
        
        data = {
            'title': 'Work',
            'address_line1': 'Kadikoy',
            'address_line2': 'Istanbul',
            'city': 'Istanbul',
            'country': 'Turkey',
            'postal_code': '34732',
        }
        response = self.create_address(data)
        response = self.create_address(data)
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

        data = {
            'email': 'firat2@email.com',
            'first_name': 'Firat',
            'last_name': 'Kizilboga',
            'password': 'Aa125423',
        }
        response = self.create_user(data)
        response = self.login_user(data['email'], data['password'])

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
        response = self.create_address(data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #list addresses
        url = reverse('address-list')
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class AddressDetailViewTest(BaseTest):
    def setUp(self):
        super().setUp()
        url = reverse('address-create')
        data = {
            'title': 'Home',
            'address_line1': 'Kadikoy',
            'address_line2': 'Istanbul',

            'city': 'Istanbul',
            'country': 'Turkey',
            'postal_code': '34732',
        }
        response = self.create_address(data)
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
        response = self.create_address(data)
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
        response = self.create_user(data)
        response = self.login_user(data['email'], data['password'])

        url = reverse('address-detail', args=["0"])
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    

class AddressDeleteViewTest(BaseTest):
    def setUp(self):
        super().setUp()
        url = reverse('address-create')
        data = {
            'title': 'Home',
            'address_line1': 'Kadikoy',
            'address_line2': 'Istanbul',
            'city': 'Istanbul',
            'country': 'Turkey',
            'postal_code': '34732',
        }
        response = self.create_address(data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_delete_address(self):
        url = reverse('address-list')
        response = self.client.post(url, format='json')
        address_id = response.data[0]['id']
        url = reverse('address-delete', args=[address_id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
