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
        #create 3 items for testing
        self.item1 = Item.objects.create(title='Item 1', price=10)
        self.item2 = Item.objects.create(title='Item 2', price=20)
        self.item3 = Item.objects.create(title='Item 3', price=30)


        data = {
            'email': 'firatkizilboga11@gmail.com',
            'first_name': 'Firat',
            'last_name': 'Kizilboga',
            'password': 'Aa125423',
        }
        self.create_user(data)
        self.login_user(data['email'], data['password'])
        self.create_address({
            'title': 'Home',
            'address_line1': '1234 Main St',
            'address_line2': 'Apt 1',
            'city': 'Los Angeles',
            'neighborhood': 'Hollywood',
            'postal_code': '90028',
            'country': 'USA',
        })

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
    
    def create_item(self, title, price):
        data = {
            'title': title,
            'price': price,
        }
        url = reverse('item-create')
        response = self.client.post(url, data, format='json')
        return response

    def create_subscription(self, data):
        url = reverse('subscription-create')
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
        self.assertEqual(len(response.data),3)

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

    def test_delete_address_unauthenticated(self):
        url = reverse('address-list')
        response = self.client.post(url, format='json')
        address_id = response.data[0]['id']
        url = reverse('address-delete', args=[address_id])
        client = APIClient()
        response = client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#subscription stuff
class SubscriptionCreateViewTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.create_address(
            {
                'title': 'Home',
                'address_line1': 'Kadikoy',
                'address_line2': 'Istanbul',
                'city': 'Istanbul',
                'country': 'Turkey',
                'postal_code': '34732',
            }
        )
    
    def test_create_subscription(self):
        url = reverse('address-list')
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        address_id = response.data[0]['id']
        
        url = reverse('subscription-create')
        data = {
            'title': 'Monthly',
            'address': address_id,
            'fullfillment_frequency': 30,
        }

        response = self.create_subscription(data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_subscription_unauthenticated(self):
        url = reverse('address-list')
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        address_id = response.data[0]['id']
        
        url = reverse('subscription-create')
        data = {
            'title': 'Monthly',
            'address': address_id,
            'fullfillment_frequency': 30,
        }

        self.client = APIClient()
        response = self.create_subscription(data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
class SubscriptionListViewTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.create_subscription(
            {
                'title': 'Monthly',
                'address': 0,
                'fullfillment_frequency': 30,
            }
        )
        self.create_subscription(
            {
                'title': 'Weekly',
                'address': 0,
                'fullfillment_frequency': 7,
            }
        )
        self.client = APIClient()
        data = {
                'email': 'firat2@gmail.com',
                'first_name': 'Firat',
                'last_name': 'Kizilboga',
                'password': 'Aa125423',
            }
        self.create_user(
            data
        )
        self.login_user(data['email'], data['password'])
        self.create_address
        (
            {
                'title': 'Home',
                'address_line1': 'Kadikoy',
                'address_line2': 'Istanbul',
                'city': 'Istanbul',
                'country': 'Turkey',
                'postal_code': '34732',
            }
        )

        self.create_subscription(
            {
                'title': 'Monthly',
                'address': 1,
                'fullfillment_frequency': 30,
            }
        )

    def test_list_subscription(self):
        url = reverse('subscription-list')
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_subscription_unauthenticated(self):
        url = reverse('subscription-list')
        client = APIClient()
        response = client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class SubscriptionDetailViewTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.create_address({
            'title': 'Home',
            'address_line1': '1234 Main St',
            'address_line2': 'Apt 1',
            'city': 'Los Angeles',
            'neighborhood': 'Hollywood',
            'postal_code': '90028',
            'country': 'USA',
        })

        response = self.create_subscription(
            {
                'title': 'Monthly',
                'address': 2,
                'fullfillment_frequency': 30,
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.create_subscription(
            {
                'title': 'Monthly',
                'address': 1,
                'fullfillment_frequency': 30,
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_detail_subscription(self):
        url = reverse('subscription-list')
        response = self.client.post(url, format='json')
        subscription_id = response.data[0].get('id')
        url = reverse('subscription-detail', args=[subscription_id])
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Monthly')
    
    
    def test_detail_subscription_unauthenticated(self):
        url = reverse('subscription-detail', args=[1])
        client = APIClient()
        response = client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_detail_subscription_does_not_exist(self):
        url = reverse('subscription-detail', args=[100])
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_detail_subscription_does_not_belong_to_user(self):
        #create a user
        self.client = APIClient()
        data = {
                'email': 'f2@gmail.com',
                'first_name': 'Firat',
                'last_name': 'Kizilboga',
                'password': 'Aa125423',
            }
        self.create_user(
            data
        )
        self.login_user(data['email'], data['password'])
        self.create_address
        (
            {
                'title': 'Home',
                'address_line1': 'Kadikoy',
                'address_line2': 'Istanbul',
                'city': 'Istanbul',
                'country': 'Turkey',
                'postal_code': '34732',
            }
        )
        self.create_subscription(
            {
                'title': 'Monthly',
                'address': 1,
                'fullfillment_frequency': 30,
            }
        )

        #reach to the subscription detail page 0
        url = reverse('subscription-detail', args=[1])
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    

class SubscriptionDeleteViewTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.create_subscription({
            'title': 'Monthly',
            'address': 1,
            'fullfillment_frequency': 30,
        })
        self.create_subscription({
            'title': 'Weekly',
            'address': 1,
            'fullfillment_frequency': 7,
        })

    def test_delete_subscription(self):
        url = reverse('subscription-delete', args=[1])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Subscription.objects.count(), 1)
    
    def test_delete_subscription_unauthenticated(self):
        url = reverse('subscription-delete', args=[1])
        client = APIClient()
        response = client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Subscription.objects.count(), 2)
    
    def test_delete_subscription_does_not_exist(self):
        url = reverse('subscription-delete', args=[100])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Subscription.objects.count(), 2)
    
    def test_delete_subscription_does_not_belong_to_user(self):
        #create a user
        self.client = APIClient()
        data = {
                'email': 'f2@gmail.com',
                'first_name': 'Firat',
                'last_name': 'Kizilboga',
                'password': 'Aa125423',
            }
        self.create_user(
            data
        )
        self.login_user(data['email'], data['password'])
        url = reverse('subscription-delete', args=[1])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class SubscriptionItemsViewTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.create_subscription({
            'title': 'Monthly',
            'address': 1,
            'fullfillment_frequency': 30,
        })
    
    def test_add_subscription_item(self):
        url = reverse('subscription-item-add', args=[1])
        data = {
            'item': 1,
            'quantity': 5
        }
        response = self.client.post(url,data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {
            'item': 2,
            'quantity': 1
        }
        response = self.client.post(url,data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {
            'item': 3,
            'quantity': 2
        }
        response = self.client.post(url,data, format='json')    
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #add a second subscription
        self.create_subscription({
            'title': 'Weekly',
            'address': 1,
            'fullfillment_frequency': 7,
        })
        url = reverse('subscription-item-add', args=[2])
        data = {
            'item': 1,
            'quantity': 5
        }
        response = self.client.post(url,data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        #total price is 5*10 + 1*20 + 2*30 = 130
        #get the subscription
        url = reverse('subscription-detail', args=[1])
        response = self.client.post(url, format='json')

        total_price = int(response.data.get('total'))
        self.assertEqual(total_price, 130)

    def test_add_subscription_item_unauthenticated(self):
        url = reverse('subscription-item-add', args=[1])
        data = {
            'item': 1,
            'quantity': 5
        }
        client = APIClient()
        response = client.post(url,data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_subscription_does_not_exist(self):
        url = reverse('subscription-item-add', args=[100])
        data = {
            'item': 1,
            'quantity': 5
        }
        response = self.client.post(url,data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_add_subscription_does_not_belong_to_user(self):
        #create a user
        self.client = APIClient()
        data = {
                'email': 'f2@gmail.com',
                'first_name': 'Firat',
                'last_name': 'Kizilboga',
                'password': 'Aa125423',
            }
        self.create_user(
            data
        )
        self.login_user(data['email'], data['password'])
        url = reverse('subscription-item-add', args=[1])
        data = {
            'item': 1,
            'quantity': 5
        }
        response = self.client.post(url,data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_add_subscription_item_does_not_exist(self):
        url = reverse('subscription-item-add', args=[1])
        data = {
            'item': 100,
            'quantity': 5
        }
        response = self.client.post(url,data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_add_subscription_item_quantity_zero(self):
        url = reverse('subscription-item-add', args=[1])
        data = {
            'item': 1,
            'quantity': 0
        }
        response = self.client.post(url,data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    

    def test_remove_subscription_item(self):
        #first add an item
        url = reverse('subscription-item-add', args=[1])
        data = {
            'item': 1,
            'quantity': 5
        }
        response = self.client.post(url,data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #remove the item
        url = reverse('subscription-item-remove', args=[1])
        data = {
            'item': 1,
            'quantity': 5
        }
        response = self.client.delete(url,data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        #get the subscription
        url = reverse('subscription-detail', args=[1])
        response = self.client.post(url, format='json')

        total_price = int(response.data.get('total'))
        self.assertEqual(total_price, 0)

 
    def test_remove_subscription_item_unauthenticated(self):
        url = reverse('subscription-item-remove', args=[1])
        data = {
            'item': 1,
            'quantity': 5
        }
        client = APIClient()
        response = client.delete(url,data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_remove_subscription_does_not_exist(self):
        url = reverse('subscription-item-remove', args=[100])
        data = {
            'item': 1,
            'quantity': 5
        }
        response = self.client.delete(url,data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_remove_subscription_does_not_belong_to_user(self):
        #create a user
        self.client = APIClient()
        data = {
                'email': 'f2@gmail.com',
                'first_name': 'Firat',
                'last_name': 'Kizilboga',
                'password': "Aa125423",
            }
        self.create_user(
            data
        )
        self.login_user(data['email'], data['password'])
        url = reverse('subscription-item-remove', args=[1])
        data = {
            'item': 1,
            'quantity': 5
        }
        response = self.client.delete(url,data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    #list all subscriptions
    def test_list_subscriptions(self):
        url = reverse('subscription-list')
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_list_subscriptions_unauthenticated(self):
        url = reverse('subscription-list')
        client = APIClient()
        response = client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class OrderTests(BaseTest):
    def setUp(self):
        super().setUp()
        #create a subscription
        data = {
            'title': 'Monthly',
            "frequency": 30,
            "address": 1,
        }
        self.create_subscription(data)
        #add an item to the subscription
        url = reverse('subscription-item-add', args=[1])
        data = {
            'item': 1,
            'quantity': 5
        }

        response = self.client.post(url,data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = reverse('order-create', args=[1])
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_order(self):
        url = reverse('order-create', args=[1])
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            
    def test_create_order_unauthenticated(self):
        url = reverse('order-create', args=[1])
        client = APIClient()
        response = client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_create_order_subscription_does_not_exist(self):
        url = reverse('order-create', args=[100])
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    
    def test_create_order_subscription_does_not_belong_to_user(self):
        #create a user
        self.client = APIClient()
        data = {
                'email': 'f2@gmail.com',
                'first_name': 'Firat',
                'last_name': 'Kizilboga',
                'password': "Aa125423",
            }
        self.create_user(
            data
        )
        self.login_user(data['email'], data['password'])
        url = reverse('order-create', args=[1])
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_order_subscription_has_no_items(self):
        #remove the item
        url = reverse('subscription-item-remove', args=[1])
        data = {
            'item': 1,
            'quantity': 5
        }
        response = self.client.delete(url,data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        url = reverse('order-create', args=[1])
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_order_subscription_has_no_address(self):
        #remove the address
        url =reverse('address-delete', args=[1])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        url = reverse('order-create', args=[1])
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_list_orders(self):
        #add item
        url = reverse('subscription-item-add', args=[1])
        data = {
            'item': 2,
            'quantity': 5
        }
        response = self.client.post(url,data, format='json')
        
        #create an order
        url = reverse('order-create', args=[1])
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #list orders
        url = reverse('order-list', args=[1])
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_orders_unauthenticated(self):
        url = reverse('order-list', args=[1])
        client = APIClient()
        response = client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_list_orders_subscription_does_not_belong_to_user(self):
        #create a user
        self.client = APIClient()
        data = {
                'email': 'f2@gmail.com',
                'first_name': 'Firat',
                'last_name': 'Kizilboga',
                'password': "Aa125423",
            }
        self.create_user(
            data
        )

        self.login_user(data['email'], data['password'])
        url = reverse('order-list', args=[1])
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_orders_status_default_user(self):
        #place order
        url = reverse('order-create', args=[1])
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        responses = []

        for i in ['order-paid', 'order-shipped', 'order-delivered', 'order-cancelled']:
            url = reverse(i, args=[1,1])
            response = self.client.post(url)
            responses.append(response)
        
        print(responses)
        for i in responses:
            self.assertEqual(i.status_code, status.HTTP_200_OK)
            
    
    def test_orders_status_unauthenticated(self):
        for i in ['order-paid', 'order-shipped', 'order-delivered', 'order-cancelled']:
            url = reverse(i, args=[1,1])
            client = APIClient()

            response = client.post(url, format='json')
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        

            
        
