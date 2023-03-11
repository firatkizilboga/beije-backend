from django.shortcuts import render

# Create your views here.

from .models import User, Order, Address, Subscription
from .serializers import UserSerializer #,OrderSerializer, AddressSerializer, SubscriptionSerializer

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
    