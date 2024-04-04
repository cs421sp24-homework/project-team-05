from rest_framework import serializers
from .models import Item, UserCollection, Transaction
from user.models import CustomUser
# from ..user.models import CustomUser
from uuid import UUID
from django.core.exceptions import ObjectDoesNotExist


# Model(Item): id name description tags price user_id
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'name', 'description', 'image', 'category', 'price', 'seller', 'is_sold')
        # Below is used for test purposes, will be REMOVED in future
        # fields = ('id', 'name', 'description', 'tags', 'price',)

class ItemSerializerWithSellerName(serializers.ModelSerializer):
    displayname = serializers.SerializerMethodField()
    sellerIcon = serializers.SerializerMethodField()
    sellerLocation = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'image', 'category', 'price', 'seller', 'displayname', 'sellerIcon', 'sellerLocation', 'is_sold']

    def get_displayname(self, obj):
        return obj.seller.displayname if obj.seller else None
    
    def get_sellerIcon(self, obj):
        return obj.seller.image.url if obj.seller and obj.seller.image else None
    
    def get_sellerLocation(self, obj):
        return obj.seller.address.name if obj.seller.address.name else None

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCollection
        fields = ['user', 'item']
        
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'item_id', 'seller_id', 'buyer_id', 'price']

class TransactionDeserializer(serializers.ModelSerializer):
    item_name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    # category = serializers.SerializerMethodField()
    seller_name = serializers.SerializerMethodField()
    seller_icon = serializers.SerializerMethodField()
    buyer_name = serializers.SerializerMethodField()
    buyer_icon = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ['id', 'item_id', 'item_name','description', 'image', 
                  'price', 'seller_id', 'seller_name', 'seller_icon', 
                  'buyer_id', 'buyer_name', 'buyer_icon']

    def get_item_name(self, obj):
        item = Item.objects.get(id = obj.item_id)
        print(item.name)
        return item.name
    
    def get_description(self, obj):
        item = Item.objects.get(id = obj.item_id)
        print(item.description)
        return item.description
    
    def get_image(self, obj):
        item = Item.objects.get(id = obj.item_id)
        if item.image:
            return item.image.url
        return None
    
    def get_seller_name(self, obj):
        user = CustomUser.objects.get(id = obj.seller_id)
        print(user.displayname)
        return user.displayname
    
    def get_seller_icon(self, obj):
        user = CustomUser.objects.get(id = obj.seller_id)
        if user.image:
            return user.image.url
        return None
    
    def get_buyer_name(self, obj):
        user = CustomUser.objects.get(id = obj.buyer_id)
        print(user.displayname)
        return user.displayname
    
    def get_buyer_icon(self, obj):
        user = CustomUser.objects.get(id = obj.buyer_id)
        if user.image:
            return user.image.url
        return None