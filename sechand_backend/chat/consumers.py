from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async
import json
from .models import Message, Room
from .serializers import MessageSerializer
from django.conf import settings
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        print("connect user, ", self.user_id)

        # if self.user.is_active:
        #     self.rooms = await self.get_user_rooms(self.user)
        
        self.rooms = await self.get_user_rooms(self.user_id)

        for room in self.rooms:
            room_group_name = 'chat_%s' % room.id
            print("connect room id, ", room.id)
            print("connect group name, ", room_group_name)

            # Join room group
            await self.channel_layer.group_add(
                room_group_name,
                self.channel_name
            )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        for room in self.rooms:
            room_group_name = 'chat_%s' % room.id
            await self.channel_layer.group_discard(
                room_group_name,
                self.channel_name
            )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', '')
        sender_web = text_data_json.get('sender', '')
        room_id = text_data_json.get('room_id', '')
        room_group_name = 'chat_%s' % room_id

        message = await self.SaveMessage(room_id, sender_web, message)
        print("receive ", message)
        
        # Send message to room group
        await self.channel_layer.group_send(
            room_group_name,
            {
                'type': 'chat_message',
                'content': message['content'],
                'sender': message['sender'],
                'timestamp': message['timestamp'],
                'room_id': room_id,
            }
        )

    async def SaveMessage(self, room_id, sender_id, message_text):
        # This helper method saves the message to the database
        try:
            room = await sync_to_async(Room.objects.get)(id=room_id)
            user = await sync_to_async(UserModel.objects.get)(id=sender_id)
            message = await sync_to_async(Message.objects.create)(
                room=room,
                sender=user,
                content=message_text
            )
            print(f"Message saved successfully: {message_text}")
            # Serialize the message
            serialized_message = await sync_to_async(MessageSerializer)(message)
            return serialized_message.data
        except Exception as e:
            print(f"Error saving message: {e}")

    # Receive message from room group
    async def chat_message(self, event):
        message = event['content']
        sender = event['sender']
        timestamp = event['timestamp']
        room_id = event['room_id']
        print(f"Broadcasting message: {message} from sender: {sender}")

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'content': message,
            'sender': sender,
            'timestamp': timestamp,
            'room_id': room_id,
        }))
    

    async def get_user_rooms(self, user_id):
        rooms = await sync_to_async(list)(Room.objects.filter(users__contains=[user_id]))
        return rooms