# from django.test import TestCase
# from post.models import Item, UserCollection, Transaction
# from decimal import Decimal
# from django.contrib.auth import get_user_model
# import uuid

# User = get_user_model()

# class ItemModelTest(TestCase):
#     def setUp(self):
#         # Set up non-modified objects used by all test methods
#         # Set up a new user for each test
#         self.user = User.objects.create_user(username='testuser', password='testpass123', email='test@test.com')
#         self.item = Item.objects.create(
#             name='Test Item',
#             description='Test Item description',
#             category='Test category',
#             price=10.01,
#             seller=self.user
#         )
    
#     def test_item_creation(self):
#         item = Item.objects.get(name='Test Item')
#         self.assertEqual(item.description, 'Test Item description')
#         self.assertEqual(item.category, 'Test category')
#         self.assertEqual(item.price, Decimal('10.01'))
#         self.assertEqual(item.seller, self.user)
#         self.assertNotEqual(item.id, "")
#         self.assertFalse(item.is_sold)
    
#     def test_item_valid_uuid(self):
#         item = Item.objects.get(name='Test Item')
#         self.assertIsInstance(item.id, uuid.UUID)


# class CollectionModelTest(TestCase):
#     def setUp(self):
#         # Set up non-modified objects used by all test methods
#         # Set up a new user for each test
#         self.user = User.objects.create_user(username='testuser', password='testpass123', email='test@test.com')
#         self.collection = UserCollection.objects.create(
#             user = self.user,
#             item = "03d9f92f-5f63-4f42-a4fe-f7c06693f5ff"
#         )
    
#     def test_collection_creation(self):
#         collection = UserCollection.objects.get(item='03d9f92f-5f63-4f42-a4fe-f7c06693f5ff')
#         self.assertEqual(collection.user, self.user)
#         self.assertEqual(str(collection.item), '03d9f92f-5f63-4f42-a4fe-f7c06693f5ff')
    
#     def test_collection_valid_uuid(self):
#         collection = UserCollection.objects.get(item='03d9f92f-5f63-4f42-a4fe-f7c06693f5ff')
#         self.assertIsInstance(collection.item, uuid.UUID)


# class TransactionModelTest(TestCase):
#     def setUp(self):
#         # Set up non-modified objects used by all test methods
#         # Set up a new user for each test
#         self.seller = User.objects.create_user(username='testseller', password='seller1234', email='testseller@test.com')
#         self.buyer = User.objects.create_user(username='testbuyer', password='buyer1234', email='testbuyer@test.com')
#         self.item = Item.objects.create(
#             name='Test Item',
#             description='Test Item description',
#             category='Test category',
#             price=2233.44,
#             seller=self.seller
#         )
#         self.transaction = Transaction.objects.create(
#             item_id = self.item.id,
#             seller_id = self.seller.id,
#             buyer_id = self.buyer.id,
#             price = 2233.44
#         )
    
#     def test_transaction_creation(self):
#         transaction = Transaction.objects.get(item_id = self.item.id)
#         self.assertEqual(transaction.seller_id, self.seller.id)
#         self.assertEqual(transaction.buyer_id, self.buyer.id)
#         self.assertIsInstance(transaction.price, Decimal)
#         self.assertEqual(str(transaction.price), '2233.44')

    
#     def test_transaction_valid_uuid(self):
#         transaction = Transaction.objects.get(item_id = self.item.id)
#         self.assertIsInstance(transaction.id, uuid.UUID)