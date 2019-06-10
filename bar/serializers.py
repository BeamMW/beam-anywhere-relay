from .models import *
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("user_id", "username", "msgr_type", "push_token", "wallet_address")


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = {"amount", "fee", "send_from", "push_type"}


class NotificationItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
