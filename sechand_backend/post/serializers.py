from rest_framework import serializers
from .models import Item, UserCollection
from django.core.exceptions import ObjectDoesNotExist


# Model(Item): id name description tags price user_id
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'name', 'description', 'category', 'price', 'seller', 'is_sold')
        # Below is used for test purposes, will be REMOVED in future
        # fields = ('id', 'name', 'description', 'tags', 'price',)

class ItemSerializerWithSellerName(serializers.ModelSerializer):
    displayname = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'category', 'price', 'seller', 'displayname', 'is_sold']

    def get_displayname(self, obj):
        return obj.seller.displayname if obj.seller else None

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCollection
        fields = ['user', 'item']
    
class CollectionDeserializer(serializers.ModelSerializer):
    item_details = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()

    class Meta:
        model = UserCollection
        fields = ['user_id', 'item_details']

    def get_user_id(self, obj):
        return obj.user.id if obj.user else None
    
    def get_item_details(self, obj):
        try:
            # Assuming 'seller' is now a field storing user identifier directly
            item_instance = Item.objects.get(id=obj.item)
            return ItemSerializerWithSellerName(item_instance).data
        except ObjectDoesNotExist:
            return None