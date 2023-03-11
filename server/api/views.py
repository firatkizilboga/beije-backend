from django.shortcuts import render

# Create your views here.

from .models import User, Order, Address, Subscription
from .serializers import UserSerializer, UserLoginSerializer #,OrderSerializer, AddressSerializer, SubscriptionSerializer

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
            return Response(serializer.errors, status=status.HTTP_400_UNAUTHORIZED)

        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
