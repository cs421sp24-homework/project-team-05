from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import VerifyEmailCode, ResetPasswordCode, Address, UserPurchase
from post.serializers import ItemSerializerWithSellerName

UserModel = get_user_model()

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'name', 'street', 'zipcode', 'latitude', 'longitude']


class CustomUserSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)

    class Meta:
        model = UserModel
        fields = ['id', 'username', 'email', 'address', 'displayname', 'image', 'phone', 'is_visible']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class CustomUserSerializerSimple(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id', 'displayname', 'image']


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

class PurchaseHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPurchase
        fields = ['user', 'item']
    
class PurchaseHistoryDeserializer(serializers.ModelSerializer):
    item = ItemSerializerWithSellerName(read_only=True)
    user_id = serializers.SerializerMethodField()

    class Meta:
        model = UserPurchase
        fields = ['user_id', 'item']

    def get_user_id(self, obj):
        return obj.user.id if obj.user else None