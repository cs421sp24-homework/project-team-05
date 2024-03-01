from django.test import TestCase
from post.models import Item
from decimal import Decimal
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class ItemModelTest(TestCase):
    def setUp(self):
        # Set up non-modified objects used by all test methods
        # Set up a new user for each test
        self.user = User.objects.create_user(username='testuser', password='testpass123', email='test@test.com')
        self.item = Item.objects.create(
            name='Test Item',
            description='Test Item description',
            category='Test category',
            price=10.01,
            seller=self.user
        )
    
    
    def test_item_creation(self):
        item = Item.objects.get(name='Test Item')
        self.assertEqual(item.description, 'Test Item description')
        self.assertEqual(item.category, 'Test category')
        self.assertEqual(item.price, Decimal('10.01'))
        self.assertEqual(item.seller, self.user)
        self.assertNotEqual(item.id, "")
        self.assertFalse(item.is_sold)
    
    def test_item_valid_uuid(self):
        item = Item.objects.get(name='Test Item')
        self.assertIsInstance(item.id, uuid.UUID)

    