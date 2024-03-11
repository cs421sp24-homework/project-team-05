from rest_framework import serializers
from .models import Room, Message
from user.models import CustomUser
from user.serializers import CustomUserSerializer

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'users')


class MessageSerializer(serializers.ModelSerializer):
    sender = CustomUserSerializer(read_only=True)
    timestamp = serializers.DateTimeField(format='%m/%d/%Y %H:%M')

    class Meta:
        model = Message
        fields = ('room', 'sender', 'content', 'timestamp')


class RoomSerializerWithMessages(serializers.ModelSerializer):
    # user = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    messages = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ('id', 'created_at', 'name', 'messages', 'last_message')
    
    # def get_user(self, obj):
    #     user = self.context['request'].user
    #     return CustomUserSerializer(user).data

    def get_name(self, obj):
        user = self.context['request'].user
        if user.id == obj.users[0]:
            other_user = CustomUser.objects.get(id=obj.users[1])
        else:
            other_user = CustomUser.objects.get(id=obj.users[0])
        return other_user.displayname
    
    def get_messages(self, obj):
        messages = Message.objects.filter(room=obj.id).order_by('timestamp')
        return MessageSerializer(messages, many=True).data
    
    def get_last_message(self, obj):
        last_message = obj.messages.last()
        if last_message:
            return MessageSerializer(last_message).data
        else:
            return None