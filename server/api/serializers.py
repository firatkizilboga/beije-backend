#serializers.py

from rest_framework import serializers
from .models import User, Order, Address, Subscription

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

