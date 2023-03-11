#serializers.py

from rest_framework import serializers
from .models import User, Order, Address, Subscription, Item, SubscriptionItem
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
    
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'address',
            'items',
            'total',
            'created_at',
            'updated_at',
            'is_active'
        ]
        read_only_fields = ['user','id','created_at','updated_at','is_active']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = [
            'id',
            'user',
            'address',
            'title',
            'fullfillment_frequency',
            'total',
            'start_date',
            'is_active'
        ]
        read_only_fields = ['user','id','start_date','is_active','total']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
class ItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = [
            'title',
            'price',
        ]

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = [
            'id',
            'title',
            'price',
        ]
        read_only_fields = ['id','title','price']
    

class SubscriptionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionItem
        fields = [
            'id',
            'item',
            'quantity',
        ]
        read_only_fields = ['id','subscription']

    def create(self, validated_data):
        #get the subscription from the context
        
        validated_data['subscription'] = Subscription.objects.get(id=self.context['subscription'])
        return super().create(validated_data)

    def validate(self, validated_data):
        #check if the related subscription is active and exists
        if not Subscription.objects.filter(id=self.context['subscription'], is_active=True).exists():
            raise serializers.ValidationError('Subscription is not active')

        #check if the related subscription belongs to the user making the request
        if not Subscription.objects.filter(id=self.context['subscription'], user=self.context['request'].user).exists():
            raise serializers.ValidationError('Subscription does not belong to user')
        
        #check if the related item exists
        if not Item.objects.filter(id=self.context['subscription']).exists():
            raise serializers.ValidationError('Item does not exist')
        
        #check if the quantity is greater than 0
        if validated_data['quantity'] < 1:
            raise serializers.ValidationError('Quantity must be greater than 0')
        
        return validated_data
        
        
