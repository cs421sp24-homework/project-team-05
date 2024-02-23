from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import VerificationCode

UserModel = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id', 'username', 'email', 'location']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class VerificationCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationCode
        fields = ['user', 'code', 'created_at']
        read_only_fields = ['created_at']