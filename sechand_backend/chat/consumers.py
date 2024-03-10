from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'chat_%s' % self.room_id

        print(self.room_id)
        print(self.room_group_name)

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
        sender = text_data_json.get('sender', '')

        # await SaveMessage(self.room_id, sender, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # async def SaveMessage(self, room_id, sender_username, message):
    #     # This helper method saves the message to the database
    #     try:
    #         room = await sync_to_async(Room.objects.get)(id=room_id)
    #         sender = await sync_to_async(settings.AUTH_USER_MODEL.objects.get)(username=sender_username)
    #         await sync_to_async(Message.objects.create)(
    #             room=room,
    #             sender=sender,
    #             content=message
    #         )
    #     except Exception as e:
    #         print(f"Error saving message: {e}")

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
