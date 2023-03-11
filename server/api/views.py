from django.shortcuts import render

# Create your views here.

from .models import User, Order, Address, Subscription
from .serializers import *

#import tokenauthentication and isauthenticated
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication

#import apiview
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

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

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

#user has to be token authenticated
class AddressCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AddressSerializer(data=request.data,context={'request': request})
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
        serializer = SubscriptionSerializer(data=request.data,context={'request': request})
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
    #make sure user is staff
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        serializer = ItemSerializer(data=request.data,context={'request': request})
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
    #make sure user is staff
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
        serializer = SubscriptionItemSerializer(data=request.data,context={'request': request, 'subscription': pk})
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
        subscriptionitem = SubscriptionItem.objects.filter(subscription=subscription)
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
class OrderCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = OrderSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, pk, order_pk):
        try:
            subscription = Subscription.objects.get(id=pk)
            order = Order.objects.filter(Subscription=subscription)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if order.user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)

class OrderDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, pk, order_pk):
        try:
            subscription = Subscription.objects.get(id=pk)
            order = Order.objects.get(id=order_pk, Subscription=subscription)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if order.user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)

class OrderPaidView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, pk, order_pk):
        try:
            subscription = Subscription.objects.get(id=pk)
            order = Order.objects.get(id=order_pk, Subscription=subscription)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if order.user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        order.pay()
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)
    
class OrderShippedView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, pk, order_pk):
        try:
            subscription = Subscription.objects.get(id=pk)
            order = Order.objects.get(id=order_pk, Subscription=subscription)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if order.user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        order.ship()
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)

class OrderDeliveredView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, pk, order_pk):
        try:
            subscription = Subscription.objects.get(id=pk)
            order = Order.objects.get(id=order_pk, Subscription=subscription)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if order.user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        order.deliver()
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)

class OrderCancelledView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, pk, order_pk):
        try:
            subscription = Subscription.objects.get(id=pk)
            order = Order.objects.get(id=order_pk, Subscription=subscription)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if order.user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        order.cancel()
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)
    