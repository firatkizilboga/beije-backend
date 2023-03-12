from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import render


# Create your views here.

from .models import *
from .serializers import *


class UserCreateView(APIView):
    """
    Create a new user in the system
    """
    def post(self, request):
        """
        Create a new user with a given email and password
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(ObtainAuthToken):
    """
    Create a new auth token for user
    """
    serializer_class = UserLoginSerializer
    def post(self, request, *args, **kwargs):
        """handle creating user authentication tokens"""
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class AdminCreateView(APIView):
    """
    Create a new admin in the system
    """
    def post(self, request):
        """
        Create a new admin with a given email and password
        """
        serializer = AdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# user has to be token authenticated
class AddressCreateView(APIView):
    """
    Create a new address in the system
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AddressSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddressListView(APIView):
    """
    List all addresses in the system
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
            Return a list of all the existing addresses.
        """
        address = Address.objects.filter(user=request.user)
        serializer = AddressSerializer(address, many=True)
        return Response(serializer.data)


class AddressDetailView(APIView):
    """
    Retrieve a single address in the system
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        """
            Return a single address
        """
        try:
            address = Address.objects.get(id=pk)
        except Address.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if address.user != request.user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AddressSerializer(address, many=False)
        return Response(serializer.data)


class AddressDeleteView(APIView):
    """
    Delete a single address in the system
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        """
            Delete a single address
        """
        try:
            address = Address.objects.get(id=pk)
        except Address.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if address.user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionCreateView(APIView):
    """
        Create a new subscription in the system
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
            Create a new subscription with a given address and subscription type
        """
        serializer = SubscriptionSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubscriptionListView(APIView):
    """
        List all subscriptions in the system
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
            Return a list of all the existing subscriptions.
        """
        subscription = Subscription.objects.filter(user=request.user)
        serializer = SubscriptionSerializer(subscription, many=True)
        return Response(serializer.data)


class SubscriptionDetailView(APIView):
    """
        Retrieve a single subscription in the system
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        """
            Return a single subscription
        """
        try:
            subscription = Subscription.objects.get(id=pk)
        except Subscription.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if subscription.user != request.user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = SubscriptionSerializer(subscription, many=False)
        return Response(serializer.data)


class SubscriptionDeleteView(APIView):
    """
        Delete a single subscription in the system
    """


    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        """
            Handles delete requests for a subscription
        """
        try:
            subscription = Subscription.objects.get(id=pk)
        except Subscription.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if subscription.user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ItemCreateView(APIView):
    """
        Create a new item in the system
     """
    authentication_classes = [TokenAuthentication]
    # make sure user is staff
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        """
            Create a new item with a given name and price
        """
        serializer = ItemSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemListView(APIView):
    """
        List all items in the system
    """

    def get(self, request):
        """
            Return a list of all the existing items.
        """
        item = Item.objects.all()
        serializer = ItemSerializer(item, many=True)
        return Response(serializer.data)


class ItemDeleteView(APIView):
    """
        Delete a single item in the system
    """

    authentication_classes = [TokenAuthentication]
    # make sure user is staff
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request, pk):
        try:
            item = Item.objects.get(id=pk)
        except Item.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionItemAddView(APIView):
    """ 
        Add an item to a subscription
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        """
            Add an item to a subscription
        """
        try:
            subscription = Subscription.objects.get(id=pk)
        except Subscription.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if subscription.user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = SubscriptionItemSerializer(
            data=request.data, context={'request': request, 'subscription': subscription})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubscriptionItemListView(APIView):
    """
        List all items in a subscription
    """
     
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        """ 
            Return a list of all the items in a subscription    """

        try:
            subscription = Subscription.objects.get(id=pk)
        except Subscription.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if subscription.user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        subscriptionitem = SubscriptionItem.objects.filter(
            subscription=subscription)
        serializer = SubscriptionItemSerializer(subscriptionitem, many=True)
        return Response(serializer.data)


class SubscriptionItemRemoveView(APIView):
    """
        Remove an item from a subscription  
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        """ 
            Handles delete requests for a subscription item
        """
        try:
            subscriptionitem = SubscriptionItem.objects.get(id=pk)
        except SubscriptionItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if subscriptionitem.subscription.user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        subscriptionitem.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderBaseView(APIView):
    """
        Base view for order
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_subscription(self, pk):
        """
                Return a single subscription by its id  
                """
        try:
            subscription = Subscription.objects.get(id=pk)
        except Subscription.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if subscription.user != self.request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return subscription
    
    def get_order(self, pk):
        """
                Return a single order by its id
            """
        try:
            order = Order.objects.get(id=pk)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if order.subscription.user != self.request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return order
    
class OrderCreateView(OrderBaseView):
    """
        Create a new order
    """
    def post(self, request, pk):
        """
            Create a new order
        """
        subscription = self.get_subscription(pk)
        if isinstance(subscription, Response):
            return subscription
        
        #check if subscriptionitem is > 0
        if SubscriptionItem.objects.filter(subscription=subscription).count():
            Order.objects.create(subscription=subscription)
            return Response(status=status.HTTP_201_CREATED)
    
        return Response(status=status.HTTP_400_BAD_REQUEST)
        
class OrderDetailView(OrderBaseView):
    """
        Get a single order
    """
    def post(self, request, pk, order_pk):
        """
            Get a single order
        """
        subscription = self.get_subscription(pk)
        if isinstance(subscription, Response):
            return subscription
        order = self.get_order(order_pk)
        if isinstance(order, Response):
            return order
        return Response(order, status=status.HTTP_200_OK)

class OrderListView(OrderBaseView):
    """
        Get a list of orders
        """
    def post(self, request, pk):
        """
            Get a list of orders
            """
        subscription = self.get_subscription(pk)
        if isinstance(subscription, Response):
            return subscription
        orders = Order.objects.filter(subscription=subscription)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OrderPayView(OrderBaseView):
    """
        set is paid to true
    """ 
    def post(self, request, pk, order_pk):
        
        """handle the setting of is paid to true"""

        subscription = self.get_subscription(pk)
        if isinstance(subscription, Response):
            return subscription
        order = self.get_order(order_pk)
        if isinstance(order, Response):
            return order
        order.pay()
        return Response(status=status.HTTP_200_OK)

class OrderStatusView(OrderBaseView):
    """
        Get the status of an order
    """

    def post(self, request, pk, order_pk):
        """
            Get the status of an order
        """
        subscription = self.get_subscription(pk)
        if isinstance(subscription, Response):
            return subscription
        order = self.get_order(order_pk)
        if isinstance(order, Response):
            return order
        order.pay()
        return Response(status=status.HTTP_200_OK)


class OrderShipView(OrderBaseView):
    """
        Set is shipped to true
    """
    def post(self, request, pk, order_pk):
        """
            handle the setting of is shipped to true
        """
        subscription = self.get_subscription(pk)
        if isinstance(subscription, Response):
            return subscription
        order = self.get_order(order_pk)
        if isinstance(order, Response):
            return order
        order.ship()
        return Response(status=status.HTTP_200_OK)

class OrderDeliverView(OrderBaseView):
    """
        Set is delivered to true
    """
    def post(self, request, pk, order_pk):
        """
            handle the setting of is delivered to true
        """

        subscription = self.get_subscription(pk)
        if isinstance(subscription, Response):
            return subscription
        order = self.get_order(order_pk)
        if isinstance(order, Response):
            return order
        order.deliver()
        return Response(status=status.HTTP_200_OK)

class OrderCancelView(OrderBaseView):
    """
        Cancel an order
    """
    def post(self, request, pk, order_pk):
        """
            handle the setting of is delivered to true
        """
        subscription = self.get_subscription(pk)
        if isinstance(subscription, Response):
            return subscription
        order = self.get_order(order_pk)
        if isinstance(order, Response):
            return order
        order.cancel()
        return Response(status=status.HTTP_200_OK)
    