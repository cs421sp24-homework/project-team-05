from rest_framework import serializers

from .models import Item

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