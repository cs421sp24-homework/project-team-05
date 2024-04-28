from django.test import TestCase
from post.models import Item, UserCollection, Transaction
from post.models import gen_unique_filename
from decimal import Decimal
from datetime import datetime
from django.contrib.auth import get_user_model
from unittest.mock import patch
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

    def test_item_deletion(self):
        item = Item.objects.get(name='Test Item')
        item.delete()
        with self.assertRaises(Item.DoesNotExist):
            Item.objects.get(name='Test Item')

    @patch('post.models.Item.delete_s3_image')
    def test_custom_save_logic(self, mock_delete_s3_image):
        item = Item.objects.create(name='Test Item2', description='A description', category='Test category', price=11.01, seller=self.user, image='./testImg/dog-avatar.PNG')
        
        item.image = './testImg/cat-avatar.png'
        item.save()
        
        mock_delete_s3_image.assert_called_once_with('./testImg/dog-avatar.PNG')

    @patch('post.models.Item.delete_s3_image')
    def test_image_deletion_on_item_deletion(self, mock_delete_s3_image):
        item = Item.objects.create(name='Test Item2', description='A description', category='Test category', price=11.01, seller=self.user, image='./testImg/dog-avatar.PNG')

        item.delete()
        
        self.assertTrue(mock_delete_s3_image.called)
        self.assertEqual(mock_delete_s3_image.call_args[0][0].name, './testImg/dog-avatar.PNG')

    def test_is_sold_default(self):
        item = Item.objects.create(name='Test Item2', description='A description', category='Test category', price=11.01, seller=self.user, image='./testImg/dog-avatar.PNG')

        self.assertFalse(item.is_sold)

    @patch('post.models.uuid.uuid4')
    @patch('post.models.now')
    def test_gen_unique_filename(self, mock_now, mock_uuid):

        mock_now.return_value = datetime(2023, 1, 1, 12, 0)
        mock_uuid.return_value = uuid.UUID('12345678123456781234567812345678')

        expected_timestamp = '20230101_120000'
        expected_uuid = '12345678-1234-5678-1234-567812345678'

        filename = gen_unique_filename(None, 'test@file!.jpg')

        expected_filename = f"media/itemImage/{expected_timestamp}_{expected_uuid}.jpg"

        self.assertEqual(filename, expected_filename)
        

class CollectionModelTest(TestCase):
    def setUp(self):
        # Set up non-modified objects used by all test methods
        # Set up a new user for each test
        self.user = User.objects.create_user(username='testuser', password='testpass123', email='test@test.com')
        self.collection = UserCollection.objects.create(
            user = self.user,
            item = "03d9f92f-5f63-4f42-a4fe-f7c06693f5ff"
        )
    
    def test_collection_creation(self):
        collection = UserCollection.objects.get(item='03d9f92f-5f63-4f42-a4fe-f7c06693f5ff')
        self.assertEqual(collection.user, self.user)
        self.assertEqual(str(collection.item), '03d9f92f-5f63-4f42-a4fe-f7c06693f5ff')
    
    def test_collection_valid_uuid(self):
        collection = UserCollection.objects.get(item='03d9f92f-5f63-4f42-a4fe-f7c06693f5ff')
        self.assertIsInstance(collection.item, uuid.UUID)


class TransactionModelTest(TestCase):
    def setUp(self):
        # Set up non-modified objects used by all test methods
        # Set up a new user for each test
        self.seller = User.objects.create_user(username='testseller', password='seller1234', email='testseller@test.com')
        self.buyer = User.objects.create_user(username='testbuyer', password='buyer1234', email='testbuyer@test.com')
        self.item = Item.objects.create(
            name='Test Item',
            description='Test Item description',
            category='Test category',
            price=2233.44,
            seller=self.seller
        )
        self.transaction = Transaction.objects.create(
            item_id = self.item.id,
            seller_id = self.seller.id,
            buyer_id = self.buyer.id,
            price = 2233.44
        )
    
    def test_transaction_creation(self):
        transaction = Transaction.objects.get(item_id = self.item.id)
        self.assertEqual(transaction.seller_id, self.seller.id)
        self.assertEqual(transaction.buyer_id, self.buyer.id)
        self.assertIsInstance(transaction.price, Decimal)
        self.assertEqual(str(transaction.price), '2233.44')

    
    def test_transaction_valid_uuid(self):
        transaction = Transaction.objects.get(item_id = self.item.id)
        self.assertIsInstance(transaction.id, uuid.UUID)