from rest_framework import serializers
from .models import Item


class RegisterUserSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=150)
    password = serializers.CharField(required=True, min_length=8)


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['name', 'description', 'quantity', 'price']
