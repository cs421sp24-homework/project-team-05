from django.test import TestCase
from ..models import Room, Message, Notification
from ..serializers import RoomSerializer, MessageSerializer, NotificationSerializer, RoomSerializerWithMessages
from datetime import datetime
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model

User = get_user_model()

class RoomSerializerTests(TestCase):
    def setUp(self):
        # Setup test data
        self.user1 = User.objects.create_user(username='user1', password='testpassword1', email="test1@example.com")
        self.user2 = User.objects.create_user(username='user2', password='testpassword2', email="test2@example.com")
        self.room = Room.objects.create(users=[str(self.user1.id), str(self.user2.id)])

    def test_serialize_room(self):
        # Serialize the room
        serializer = RoomSerializer(instance=self.room)
        # Check that the fields are correctly serialized
        self.assertEqual(set(serializer.data.keys()), set(['id', 'users']))
        self.assertEqual(len(serializer.data['users']), 2)

class MessageSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='testpassword', email="test@example.com")
        self.room = Room.objects.create(users=[str(self.user.id)])
        self.message = Message.objects.create(room=self.room, sender=self.user, content="Hello World")

    def test_serialize_message(self):
        # Serialize the message
        serializer = MessageSerializer(instance=self.message)
        # Check that the fields are correctly serialized
        self.assertEqual(set(serializer.data.keys()), set(['room', 'sender', 'content', 'data', 'timestamp']))
        self.assertEqual(serializer.data['content'], "Hello World")

class NotificationSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='testpassword', email="test@example.com")
        self.room = Room.objects.create(users=[str(self.user.id)])
        self.notification = Notification.objects.get(user=self.user, room=self.room)

    def test_serialize_notification(self):
        # Serialize the notification
        serializer = NotificationSerializer(instance=self.notification)
        # Check that the fields are correctly serialized
        self.assertEqual(set(serializer.data.keys()), set(['user', 'room', 'count', 'active']))
        self.assertEqual(serializer.data['count'], 0)
        self.assertTrue(serializer.data['active'])