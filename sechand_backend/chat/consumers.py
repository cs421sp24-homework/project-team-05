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
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'chat_%s' % self.room_id

        print("connect room id, ", self.room_id)
        print("connect group name, ", self.room_group_name)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', '')
        sender_web = text_data_json.get('sender', '')

        message = await self.SaveMessage(self.room_id, sender_web, message)
        print("receive ", message)
        
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'content': message['content'],
                'sender': message['sender'],
                'timestamp': message['timestamp']
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
        print(f"Broadcasting message: {message} from sender: {sender}")

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'content': message,
            'sender': sender,
            'timestamp': timestamp
        }))
