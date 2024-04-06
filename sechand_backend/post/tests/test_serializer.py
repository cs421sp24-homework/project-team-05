from post.serializers import ItemSerializer, ItemSerializerWithSellerName
from post.serializers import CollectionSerializer, TransactionSerializer
from post.serializers import TransactionDeserializer
from django.test import TestCase
from post.models import Item, UserCollection, Transaction
from django.contrib.auth import get_user_model

User = get_user_model()

class ItemSerializerTest(TestCase):
    def setUp(self):
        # Set up non-modified objects used by all test methods
        # Set up a new user for each test
        self.user = User.objects.create_user(username='Serializer testuser', password='serializer123', email='serializer@test.com', displayname='test displayname')
        self.item = Item.objects.create(
            name='Serializer Test Item',
            description='Test Item description',
            category='Test category',
            price=111.01,
            seller=self.user
        )
        self.patch = { "category" : "Patch category" }
    
    def test_serialize_item(self):
        item = Item.objects.get(name='Serializer Test Item')
        serializer = ItemSerializer(item)

        self.assertEqual(serializer.data['id'], str(self.item.id))
        self.assertEqual(serializer.data['name'], 'Serializer Test Item')
        self.assertEqual(serializer.data['description'], 'Test Item description')
        self.assertEqual(serializer.data['category'], 'Test category')
        self.assertEqual(float(serializer.data['price']), 111.01)
        self.assertEqual(serializer.data['seller'], self.user.id)
        self.assertEqual(serializer.data['is_sold'], False)

    def test_serialize_partial_update(self):
        item = Item.objects.get(name='Serializer Test Item')
        serializer = ItemSerializer(item)

        self.assertEqual(serializer.data['id'], str(self.item.id))
        self.assertEqual(serializer.data['name'], 'Serializer Test Item')
        self.assertEqual(serializer.data['description'], 'Test Item description')
        self.assertEqual(serializer.data['category'], 'Test category')
        self.assertEqual(float(serializer.data['price']), 111.01)
        self.assertEqual(serializer.data['seller'], self.user.id)
        self.assertEqual(serializer.data['is_sold'], False)

        serializer = ItemSerializer(item, self.patch, partial=True)
        if serializer.is_valid():
            serializer.save()
            self.assertEqual(serializer.data['category'], 'Patch category')
        else:
            raise AssertionError("Serializer after patching information is not valid.")
        
    def test_serialize_item_with_name(self):
        item = Item.objects.get(name='Serializer Test Item')
        serializer = ItemSerializerWithSellerName(item)

        self.assertEqual(serializer.data['id'], str(self.item.id))
        self.assertEqual(serializer.data['name'], 'Serializer Test Item')
        self.assertEqual(serializer.data['description'], 'Test Item description')
        self.assertEqual(serializer.data['category'], 'Test category')
        self.assertEqual(float(serializer.data['price']), 111.01)
        self.assertEqual(serializer.data['seller'], self.user.id)
        self.assertEqual(serializer.data['is_sold'], False)
        self.assertEqual(serializer.data['displayname'], 'test displayname')

class CollectionSerializerTest(TestCase):
    def setUp(self):
        # Set up non-modified objects used by all test methods
        # Set up a new user for each test
        self.user = User.objects.create_user(username='Serializer testuser', password='serializer123', email='serializer@test.com', displayname='test displayname')
        self.item = Item.objects.create(
            name='Serializer Test Item',
            description='Test Item description',
            category='Test category',
            price=111.01,
            seller=self.user
        )
        self.collection = UserCollection.objects.create(
            user = self.user,
            item = '03d9f92f-5f63-4f42-a4fe-f7c06693f5ff'
        )
    
    def test_serialize_item(self):
        collection = UserCollection.objects.get(item='03d9f92f-5f63-4f42-a4fe-f7c06693f5ff')
        serializer = CollectionSerializer(collection)

        self.assertEqual(serializer.data['user'], self.user.id)
        self.assertEqual(serializer.data['item'], '03d9f92f-5f63-4f42-a4fe-f7c06693f5ff')

class TransactionSerializerTest(TestCase):
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

    def test_serialize_transaction(self):
        transaction = Transaction.objects.get(item_id = self.item.id)
        serializer = TransactionSerializer(transaction)
        self.assertEqual(serializer.data['item_id'], str(self.item.id))
        self.assertEqual(serializer.data['buyer_id'], self.transaction.buyer_id)
        self.assertEqual(serializer.data['seller_id'], self.transaction.seller_id)
        self.assertEqual(str(serializer.data['price']), str(self.transaction.price))

    def test_deserialize_transaction(self):
        transaction = Transaction.objects.get(item_id = self.item.id)
        serializer = TransactionDeserializer(transaction)

        self.assertEqual(serializer.data['id'], self.item.id)
        self.assertEqual(serializer.data['name'], self.item.name)
        self.assertEqual(serializer.data['description'], self.item.description)
        self.assertEqual(serializer.data['image'], None)
        self.assertEqual(str(serializer.data['price']), str(self.transaction.price))

        self.assertEqual(serializer.data['seller'], self.seller.id)
        self.assertEqual(serializer.data['displayname'], self.seller.displayname)

