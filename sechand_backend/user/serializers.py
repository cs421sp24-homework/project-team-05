from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import VerifyEmailCode, ResetPasswordCode

UserModel = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id', 'username', 'email', 'location']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class VerifyEmailCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerifyEmailCode
        fields = ['user', 'code', 'created_at']
        read_only_fields = ['created_at']


class ResetPasswordCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResetPasswordCode
        fields = ['user', 'code', 'token', 'created_at']
        read_only_fields = ['created_at']