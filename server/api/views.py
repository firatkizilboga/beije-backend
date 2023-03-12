from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.shortcuts import render

# Create your views here.

from .models import User, Order, Address, Subscription
from .serializers import *

# import tokenauthentication and isauthenticated
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication

# import apiview
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class UserCreateView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(ObtainAuthToken):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
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
    def post(self, request):
        serializer = AdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# user has to be token authenticated
class AddressCreateView(APIView):
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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        address = Address.objects.filter(user=request.user)
        serializer = AddressSerializer(address, many=True)
        return Response(serializer.data)


class AddressDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            address = Address.objects.get(id=pk)
        except Address.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if address.user != request.user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AddressSerializer(address, many=False)
        return Response(serializer.data)


class AddressDeleteView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            address = Address.objects.get(id=pk)
        except Address.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if address.user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SubscriptionSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubscriptionListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        subscription = Subscription.objects.filter(user=request.user)
        serializer = SubscriptionSerializer(subscription, many=True)
        return Response(serializer.data)


class SubscriptionDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            subscription = Subscription.objects.get(id=pk)
        except Subscription.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if subscription.user != request.user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = SubscriptionSerializer(subscription, many=False)
        return Response(serializer.data)


class SubscriptionDeleteView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            subscription = Subscription.objects.get(id=pk)
        except Subscription.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if subscription.user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ItemCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    # make sure user is staff
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        serializer = ItemSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemListView(APIView):
    def get(self, request):
        item = Item.objects.all()
        serializer = ItemSerializer(item, many=True)
        return Response(serializer.data)


class ItemDeleteView(APIView):
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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            subscriptionitem = SubscriptionItem.objects.get(id=pk)
        except SubscriptionItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if subscriptionitem.subscription.user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        subscriptionitem.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""
    path('subscription/<int:pk>/order/', OrderCreateView.as_view(), name='order-create'),
    path('subscription/<int:pk>/order/<int:order_pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('subscription/<int:pk>/order/<int:order_pk>/status/set/paid', OrderPaidView.as_view(), name='order-delete'),
    path('subscription/<int:pk>/order/<int:order_pk>/status/set/shipped', OrderShippedView.as_view(), name='order-delete'),
    path('subscription/<int:pk>/order/<int:order_pk>/status/set/delivered', OrderDeliveredView.as_view(), name='order-delete'),
    path('subscription/<int:pk>/order/<int:order_pk>/status/set/cancelled', OrderCancelledView.as_view(), name='order-delete'),
    path('subscription/<int:pk>/order/list/', OrderListView.as_view(), name='order-list'),
"""


class OrderBaseView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_subscription(self, pk):
        try:
            subscription = Subscription.objects.get(id=pk)
        except Subscription.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if subscription.user != self.request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return subscription
    
    def get_order(self, pk):
        try:
            order = Order.objects.get(id=pk)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if order.subscription.user != self.request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return order
    
class OrderCreateView(OrderBaseView):
    def post(self, request, pk):
        subscription = self.get_subscription(pk)
        if isinstance(subscription, Response):
            return subscription
        
        #check if subscriptionitem is > 0
        if SubscriptionItem.objects.filter(subscription=subscription).count():
            Order.objects.create(subscription=subscription)
            return Response(status=status.HTTP_201_CREATED)
    
        return Response(status=status.HTTP_400_BAD_REQUEST)
        
class OrderDetailView(OrderBaseView):
    def post(self, request, pk, order_pk):
        subscription = self.get_subscription(pk)
        if isinstance(subscription, Response):
            return subscription
        order = self.get_order(order_pk)
        if isinstance(order, Response):
            return order
        return Response(order, status=status.HTTP_200_OK)

class OrderListView(OrderBaseView):
    def post(self, request, pk):
        subscription = self.get_subscription(pk)
        if isinstance(subscription, Response):
            return subscription
        orders = Order.objects.filter(subscription=subscription)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OrderPayView(OrderBaseView):
    def post(self, request, pk, order_pk):
        subscription = self.get_subscription(pk)
        if isinstance(subscription, Response):
            return subscription
        order = self.get_order(order_pk)
        if isinstance(order, Response):
            return order
        order.pay()
        return Response(status=status.HTTP_200_OK)

class OrderStatusView(OrderBaseView):
    def post(self, request, pk, order_pk):
        subscription = self.get_subscription(pk)
        if isinstance(subscription, Response):
            return subscription
        order = self.get_order(order_pk)
        if isinstance(order, Response):
            return order
        order.pay()
        return Response(status=status.HTTP_200_OK)


class OrderShipView(OrderBaseView):
    def post(self, request, pk, order_pk):
        subscription = self.get_subscription(pk)
        if isinstance(subscription, Response):
            return subscription
        order = self.get_order(order_pk)
        if isinstance(order, Response):
            return order
        order.ship()
        return Response(status=status.HTTP_200_OK)

class OrderDeliverView(OrderBaseView):
    def post(self, request, pk, order_pk):
        subscription = self.get_subscription(pk)
        if isinstance(subscription, Response):
            return subscription
        order = self.get_order(order_pk)
        if isinstance(order, Response):
            return order
        order.deliver()
        return Response(status=status.HTTP_200_OK)

class OrderCancelView(OrderBaseView):
    def post(self, request, pk, order_pk):
        subscription = self.get_subscription(pk)
        if isinstance(subscription, Response):
            return subscription
        order = self.get_order(order_pk)
        if isinstance(order, Response):
            return order
        order.cancel()
        return Response(status=status.HTTP_200_OK)
    