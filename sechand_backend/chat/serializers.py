from rest_framework import serializers
from .models import Room, Message, Notification
from user.models import CustomUser
from user.serializers import CustomUserSerializerSimple
from post.models import Item
from post.serializers import ItemSerializer

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'users')


class MessageSerializer(serializers.ModelSerializer):
    sender = CustomUserSerializerSimple(read_only=True)
    timestamp = serializers.DateTimeField(format='%m/%d/%Y %H:%M')

    class Meta:
        model = Message
        fields = ('room', 'sender', 'content', 'data', 'timestamp')


class NotificationSerializer(serializers.ModelSerializer):
    user = CustomUserSerializerSimple(read_only=True)
    room = RoomSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ('user', 'room', 'count', 'active')


class RoomSerializerWithMessages(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    # name = serializers.SerializerMethodField()
    messages = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    notification = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ('id', 'user', 'messages', 'last_message', 'notification', 'items')
    
    def get_user(self, obj):
        user = self.context['request'].user
        if str(user.id) == str(obj.users[0]):
            other_user = CustomUser.objects.get(id=obj.users[1])
        else:
            other_user = CustomUser.objects.get(id=obj.users[0])
        return CustomUserSerializerSimple(other_user).data

    def get_messages(self, obj):
        messages = Message.objects.filter(room=obj.id).order_by('timestamp')
        return MessageSerializer(messages, many=True).data
    
    def get_last_message(self, obj):
        last_message = obj.messages.last()
        if last_message:
            return MessageSerializer(last_message).data
        else:
            return None
    
    def get_notification(self, obj):
        try:
            notification = Notification.objects.get(user=self.context['request'].user, room=obj)
        except Notification.DoesNotExist:
            notification = Notification.objects.create(user=self.context['request'].user, room=obj)
        
        return notification.count
    
    def get_items(self, obj):
        other_user_id = obj.users[0] if str(self.context['request'].user.id) == str(obj.users[1]) else obj.users[1]
        items = Item.objects.filter(seller__id=other_user_id, is_sold=False)
        return ItemSerializer(items, many=True).data