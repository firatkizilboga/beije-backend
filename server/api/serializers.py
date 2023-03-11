#serializers.py

from rest_framework import serializers
from .models import User, Order, Address, Subscription
from rest_framework.authtoken.serializers import AuthTokenSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'password'
        ]

    def validate(self, data):
        if len(data['password']) < 8:
            raise serializers.ValidationError('Password must be at least 8 characters long')
        return data
    
    def save(self):
        user = User(
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
        )
        password = self.validated_data['password']
        user.set_password(password)
        user.save()
        return user

from django.contrib.auth import authenticate

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(label='email')
    password = serializers.CharField(
        label='password',
        style={'input_type': 'password'},
        trim_whitespace=False
    )
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            
            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)

            if not user:
                msg = ('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = ('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
    
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields =  [
            'title',
            'address_line1',
            'address_line2',
            'city',
            'neighborhood',
            'postal_code',
            'country',
            'user',
            'id'
        ]
        read_only_fields = ['user','id']

    def validate(self, data):
        if len(data['postal_code']) < 5:
            raise serializers.ValidationError('Postal code must be at least 5 characters long')
        
        if len(data['address_line1']) < 1:
            raise serializers.ValidationError('Address line 1 must be filled')

        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)