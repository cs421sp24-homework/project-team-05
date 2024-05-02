# from django.test import TestCase
# from ..models import Room, Message, Notification
# from datetime import datetime
# from django.db.utils import IntegrityError
# from django.contrib.auth import get_user_model

# User = get_user_model()

# class RoomModelTests(TestCase):

#     def test_room_creation_triggers_notification_creation(self):
#         # Create users
#         user1 = User.objects.create(username='user1', password='testpassword123', email="test1@example.com")
#         user2 = User.objects.create(username='user2', password='testpassword123', email="test2@example.com")

#         # Create Room
#         room = Room.objects.create(users=[str(user1.id), str(user2.id)])
        
#         # Check Room creation
#         self.assertEqual(Room.objects.count(), 1)

#         # Check Notifications created for each user
#         self.assertEqual(Notification.objects.count(), 2)
#         self.assertTrue(Notification.objects.filter(user=user1, room=room).exists())
#         self.assertTrue(Notification.objects.filter(user=user2, room=room).exists())

#         # Test initial values
#         notification = Notification.objects.get(user=user1, room=room)
#         self.assertEqual(notification.count, 0)
#         self.assertTrue(notification.active)


# class MessageModelTests(TestCase):

#     def test_message_ordering(self):
#         # Setup
#         user1 = User.objects.create(username='user3', password='testpassword123', email="test3@example.com")
#         user2 = User.objects.create(username='user4', password='testpassword123', email="test4@example.com")
#         room = Room.objects.create(users=[str(user1.id), str(user2.id)])

#         # Create messages
#         message1 = Message.objects.create(room=room, sender=user1, content="First message")
#         message2 = Message.objects.create(room=room, sender=user1, content="Second message")

#         # Test ordering by timestamp
#         messages = list(Message.objects.all())
#         self.assertTrue(messages.index(message1) < messages.index(message2))


# class NotificationModelTests(TestCase):

#     def test_notification_created(self):
#         # Setup
#         user1 = User.objects.create(username='user5', password='testpassword123', email="test5@example.com")
#         user2 = User.objects.create(username='user6', password='testpassword123', email="test6@example.com")
#         room = Room.objects.create(users=[str(user1.id), str(user2.id)])

#         # Attempt to create a duplicate notification
#         with self.assertRaises(IntegrityError):
#             notification1 = Notification.objects.create(user=user1, room=room)
#             notification1.full_clean()

#     def test_notification_active_default(self):
#         # Setup
#         user1 = User.objects.create(username='user7', password='testpassword123', email="test7@example.com")
#         user2 = User.objects.create(username='user8', password='testpassword123', email="test8@example.com")
#         room = Room.objects.create(users=[str(user1.id), str(user2.id)])

#         # Create a notification
#         notification = Notification.objects.get(user=user1, room=room)

#         # Test default active status
#         self.assertTrue(notification.active)

