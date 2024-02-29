# from post.serializers import ItemSerializer, ItemSerializerWithSellerName
# from django.test import TestCase
# from post.models import Item
# from django.contrib.auth import get_user_model

# User = get_user_model()

# class ItemSerializerTest(TestCase):
#     def setUp(self):
#         # Set up non-modified objects used by all test methods
#         # Set up a new user for each test
#         self.user = User.objects.create_user(username='Serializer testuser', password='serializer123', email='serializer@test.com', displayname='test displayname')
#         self.item = Item.objects.create(
#             name='Serializer Test Item',
#             description='Test Item description',
#             category='Test category',
#             price=111.01,
#             seller=self.user
#         )
#         self.patch = { "category" : "Patch category" }
    
#     def test_serialize_item(self):
#         item = Item.objects.get(name='Serializer Test Item')
#         serializer = ItemSerializer(item)

#         self.assertEqual(serializer.data['id'], str(self.item.id))
#         self.assertEqual(serializer.data['name'], 'Serializer Test Item')
#         self.assertEqual(serializer.data['description'], 'Test Item description')
#         self.assertEqual(serializer.data['category'], 'Test category')
#         self.assertEqual(float(serializer.data['price']), 111.01)
#         self.assertEqual(serializer.data['seller'], self.user.id)
#         self.assertEqual(serializer.data['is_sold'], False)

#     def test_serialize_partial_update(self):
#         item = Item.objects.get(name='Serializer Test Item')
#         serializer = ItemSerializer(item)

#         self.assertEqual(serializer.data['id'], str(self.item.id))
#         self.assertEqual(serializer.data['name'], 'Serializer Test Item')
#         self.assertEqual(serializer.data['description'], 'Test Item description')
#         self.assertEqual(serializer.data['category'], 'Test category')
#         self.assertEqual(float(serializer.data['price']), 111.01)
#         self.assertEqual(serializer.data['seller'], self.user.id)
#         self.assertEqual(serializer.data['is_sold'], False)

#         serializer = ItemSerializer(item, self.patch, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             self.assertEqual(serializer.data['category'], 'Patch category')
#         else:
#             raise AssertionError("Serializer after patching information is not valid.")
        
#     def test_serialize_item_with_name(self):
#         item = Item.objects.get(name='Serializer Test Item')
#         serializer = ItemSerializerWithSellerName(item)

#         self.assertEqual(serializer.data['id'], str(self.item.id))
#         self.assertEqual(serializer.data['name'], 'Serializer Test Item')
#         self.assertEqual(serializer.data['description'], 'Test Item description')
#         self.assertEqual(serializer.data['category'], 'Test category')
#         self.assertEqual(float(serializer.data['price']), 111.01)
#         self.assertEqual(serializer.data['seller'], self.user.id)
#         self.assertEqual(serializer.data['is_sold'], False)
#         self.assertEqual(serializer.data['displayname'], 'test displayname')