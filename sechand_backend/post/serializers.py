from rest_framework import serializers

from .models import Item

# Model(Item): id name description tags price user_id
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'name', 'description', 'tags', 'price', 'user_id',)


