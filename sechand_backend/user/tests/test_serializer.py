# from django.test import TestCase
# from ..models import Address, CustomUser
# from ..serializers import AddressSerializer, CustomUserSerializer

# class AddressSerializerTest(TestCase):

#     def setUp(self):
#         self.address_attributes = {
#             'name': 'Test Address',
#             'street': '123 Main St',
#             'zipcode': '12345',
#             'latitude': 40.712776,
#             'longitude': -74.005974,
#         }
#         self.address = Address.objects.create(**self.address_attributes)
#         self.serializer = AddressSerializer(instance=self.address)

#     def test_contains_expected_fields(self):
#         data = self.serializer.data
#         self.assertEqual(set(data.keys()), set(['id', 'name', 'street', 'zipcode', 'latitude', 'longitude']))

#     def test_field_content(self):
#         data = self.serializer.data
#         self.assertEqual(data['name'], self.address_attributes['name'])
#         self.assertEqual(data['street'], self.address_attributes['street'])
#         self.assertEqual(data['zipcode'], self.address_attributes['zipcode'])
#         self.assertAlmostEqual(float(data['latitude']), self.address_attributes['latitude'])
#         self.assertAlmostEqual(float(data['longitude']), self.address_attributes['longitude'])

# class CustomUserSerializerTest(TestCase):

#     def setUp(self):
#         self.user_attributes = {
#             'username': 'testuser',
#             'email': 'test@example.com',
#             'phone': '1234567890',
#             'displayname': 'Test User',
#             'is_visible': True
#         }
#         self.user = CustomUser.objects.create_user(**self.user_attributes)
#         self.serializer = CustomUserSerializer(instance=self.user)

#     def test_contains_expected_fields(self):
#         data = self.serializer.data
#         self.assertEqual(set(data.keys()), set(['id', 'username', 'email', 'address', 'displayname', 'image', 'phone', 'is_visible']))

#     def test_field_content(self):
#         data = self.serializer.data
#         self.assertEqual(data['username'], self.user_attributes['username'])
#         self.assertEqual(data['email'], self.user_attributes['email'])
#         self.assertEqual(data['phone'], self.user_attributes['phone'])
#         self.assertEqual(data['displayname'], self.user_attributes['displayname'])
#         self.assertEqual(data['is_visible'], self.user_attributes['is_visible'])
#         self.assertIsNone(data['address'])  # Assuming the user has no related address at setup
