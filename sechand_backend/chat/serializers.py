from rest_framework import serializers
from .models import Room, Message
from user.models import CustomUser
from user.serializers import CustomUserSerializerSimple

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'users')


class MessageSerializer(serializers.ModelSerializer):
    sender = CustomUserSerializerSimple(read_only=True)
    timestamp = serializers.DateTimeField(format='%m/%d/%Y %H:%M')

    class Meta:
        model = Message
        fields = ('room', 'sender', 'content', 'timestamp')


class RoomSerializerWithMessages(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    # name = serializers.SerializerMethodField()
    messages = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ('id', 'user', 'messages', 'last_message')
    
    def get_user(self, obj):
        user = self.context['request'].user
        # print("user, user0, user1", user.id, obj.users[0], obj.users[1])
        # print("user = user0", str(user.id) == obj.users[0])
        # print("user = user1", str(user.id) == obj.users[1])
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