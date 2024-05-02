from django.test import TestCase
from ..models import Room, Message, Notification
from ..serializers import RoomSerializer, RoomSerializerWithMessages
from post.models import Item
from datetime import datetime
from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatAPITests(APITestCase):
    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(username='user1', password='password123', email="test1@example.com")
        self.user2 = User.objects.create_user(username='user2', password='password123', email="test2@example.com")
        self.user3 = User.objects.create_user(username='user3', password='password123', email="test3@example.com")
        self.room = Room.objects.create(users=[self.user1.id, self.user2.id])
        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)
    
    def create_message(self, room, sender, content="Default content"):
        return Message.objects.create(room=room, sender=sender, content=content)
    
    def test_get_empty_chat_list(self):
        url = reverse('GetChatList')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # Expect empty list when no messages exist

    def test_get_chat_list_with_messages(self):
        # Create rooms and messages
        self.create_message(room=self.room, sender=self.user1, content='Hello World')
        
        url = reverse('GetChatList')  # Ensure you have named your URL patterns
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Check if one room is returned
        self.assertEqual(response.data[0]['last_message']['content'], 'Hello World') #Check if last message is correct
    
    def test_get_chat_list_with_specific_receiver(self):
        # Create room with specific receiver
        self.create_message(room=self.room, sender=self.user1)
        url = reverse('GetChatListWithReceiver', kwargs={'receiver_id': self.user2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['chat_list']), 1)  # Verify that the room with the receiver is returned
        self.assertEqual(response.data['active_chat'], 0)  # Verify that the room is set as active

    def test_create_new_room_with_receiver(self):
        url = reverse('GetChatListWithReceiver', kwargs={'receiver_id': self.user3.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Room.objects.filter(users__contains=[self.user3.id]).exists())  # Verify room creation

    def test_send_item_link(self):
        # Create an item
        item = Item.objects.create(name="Test Item", description="Test Description", seller=self.user1, price=100.00)
        url = reverse('SendItemLink', args=[self.user2.id, item.id])

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'item link sent')
        
        # Check if message is created
        self.assertTrue(Message.objects.filter(content='Hi, I\'m interested in this item.').exists())
        self.assertTrue(Message.objects.filter(data__name='Test Item').exists())

    def test_new_message_notification(self):
        url = reverse('NewMessageNotification')
        response = self.client.post(url, {'room_id': self.room.id, 'receiver_id': self.user2.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Notification.objects.get(user=self.user2, room=self.room).count, 1)

    def test_send_item_link_creates_message_and_notification(self):
        item = Item.objects.create(name="Test Item", description="Test Description", seller=self.user1, price=100.00)
        url = reverse('SendItemLink', kwargs={'receiver_id': self.user2.id, 'item_id': item.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Message.objects.filter(data__id=str(item.id)).exists())
        self.assertEqual(Notification.objects.get(user=self.user2).count, 1)

    def test_new_message_notification_increments_count(self):
        url = reverse('NewMessageNotification')
        self.client.post(url, {'room_id': self.room.id, 'receiver_id': self.user2.id})
        self.assertEqual(Notification.objects.get(user=self.user2, room=self.room).count, 1)

    def test_read_message_notification_resets_count(self):
        for i in range(5):
            self.create_message(room=self.room, sender=self.user1)

        url = reverse('ReadMessageNotification')
        notification = Notification.objects.get(user=self.user1, room=self.room)
        self.client.post(url, {'room_id': self.room.id})
        notification.refresh_from_db()
        self.assertEqual(notification.count, 0)
        self.assertFalse(notification.active)

    def test_activate_notification(self):
        notification = Notification.objects.get(user=self.user1, room=self.room)
        notification.active = False
        url = reverse('ActivateNotification')
        self.client.post(url, {'room_id': self.room.id})
        notification.refresh_from_db()
        self.assertTrue(notification.active)
