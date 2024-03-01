from rest_framework import serializers

from .models import Item, UserCollection, UserPurchase

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
    item = ItemSerializerWithSellerName(read_only=True)
    user_id = serializers.SerializerMethodField()

    class Meta:
        model = UserCollection
        fields = ['user_id', 'item']

    def get_user_id(self, obj):
        return obj.user.id if obj.user else None