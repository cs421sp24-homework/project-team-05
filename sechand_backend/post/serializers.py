from rest_framework import serializers

from .models import Item

# Model(Item): id name description tags price user_id
class SolelyItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'name', 'description', 'tags', 'price', 'user_id', 'is_sold')
        # Below is used for test purposes, will be REMOVED in future
        # fields = ('id', 'name', 'description', 'tags', 'price',)

class ItemSerializerWithSellerName(serializers.ModelSerializer):
    displayname = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'tags', 'price', 'user_id', 'displayname', 'is_sold']

    def get_displayname(self, obj):
        return obj.user_id.displayname if obj.user_id else None