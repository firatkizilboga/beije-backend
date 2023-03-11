from django.shortcuts import render

# Create your views here.

from .models import User, Order, Address, Subscription
from .serializers import UserSerializer, UserLoginSerializer,AddressSerializer #,OrderSerializer, , SubscriptionSerializer

#import tokenauthentication and isauthenticated
from rest_framework.permissions import IsAuthenticated
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

