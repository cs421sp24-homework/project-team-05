# from django.test import TestCase, Client
# from django.urls import reverse
# from django.contrib.auth import get_user_model
# from post.models import Item
# from user.models import Address
# from rest_framework import status
# from rest_framework.test import APIClient
# from decimal import Decimal

# User = get_user_model()

# # class GetAllUserItemsTest(TestCase):
# #     def setUp(self):
# #         self.client = APIClient()
# #         self.user = User.objects.create_user(username='testuser', password='testpass')
# #         self.url = reverse('GetAllUserItems')

# #     def test_get_all_user_items_no_auth(self):
# #         response = self.client.get(self.url)
# #         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# #     def test_get_all_user_items_with_auth(self):
# #         self.client.force_authenticate(user=self.user)
# #         response = self.client.get(self.url)
# #         self.assertEqual(response.status_code, status.HTTP_200_OK)

# # class GetAllItemsTest(TestCase):
# #     def setUp(self):
# #         self.client = APIClient()
# #         self.url = reverse('GetAllItems')

# #     def test_get_all_items_valid_count(self):
# #         response = self.client.get(self.url, {'count': 5})
# #         self.assertEqual(response.status_code, status.HTTP_200_OK)

# # class ProcessSingleItemTest(TestCase):
# #     def setUp(self):
# #         self.client = APIClient()
# #         self.user = User.objects.create_user(username='testuser', password='testpass')
# #         self.item = Item.objects.create(name='Test Item', description='Test Desc', category='Test Category', price=10.01, seller=self.user)
# #         self.url = reverse('ProcessSingleItem', kwargs={'item_id': self.item.id})

# #     def test_get_single_item(self):
# #         response = self.client.get(self.url)
# #         self.assertEqual(response.status_code, status.HTTP_200_OK)

# #     def test_delete_single_item_with_auth(self):
# #         self.client.force_authenticate(user=self.user)
# #         response = self.client.delete(self.url)
# #         self.assertEqual(response.status_code, status.HTTP_200_OK)

# class SearchItemsTest(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.url = reverse('SearchItems')  # Replace 'search_items' with the actual URL name in your urls.py
#         # Set up user and address
#         self.user = User.objects.create_user(username='testuser', password='testpass')
#         self.address = Address.objects.create(name='Test Address', street='123 Main St', zipcode='12345', latitude=Decimal('40.7128'), longitude=Decimal('-74.0060'))
#         self.user.address = self.address
#         self.user.save()

#         self.item1 = Item.objects.create(
#             name='Math Textbook',
#             description='Description for Item 1',
#             category='Books',
#             price=Decimal('20.00'),
#             seller=self.user,
#             is_sold=False
#         )
#         self.item2 = Item.objects.create(
#             name='Baseball',
#             description='Description for Item 2',
#             category='Sporting Goods',
#             price=Decimal('50.00'),
#             seller=self.user,
#             is_sold=False
#         )
        
#     def test_search_items_with_description(self):
#         response = self.client.get(reverse('GetAllItems'))
#         self.assertEqual(len(response.json()), 2)
#         params = {'desc_text': 'Baseball', 'category': 'all'}
#         response = self.client.post(self.url, data=params)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.json()), 1)
        
#     def test_search_items_by_price_range(self):
#         params = {'desc_text': '', 'lowest_price': '5', 'highest_price': '15', 'category': 'all'}
#         response = self.client.post(self.url, data=params)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.json()), 0)
#         params = {'desc_text': '', 'lowest_price': '5', 'highest_price': '25', 'category': 'all'}
#         response = self.client.post(self.url, data=params)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.json()), 1)
        
        
#     def test_search_items_by_category(self):
#         params = {'desc_text': '', 'category': 'Books', 'location': [], 'distance': '-1'}
#         response = self.client.post(self.url, data=params)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
