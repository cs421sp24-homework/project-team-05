from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from post.models import Item
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()

class GetAllUserItemsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.url = reverse('GetAllUserItems')

    def test_get_all_user_items_no_auth(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_all_user_items_with_auth(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetAllItemsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('GetAllItems')

    def test_get_all_items_valid_count(self):
        response = self.client.get(self.url, {'count': 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class ProcessSingleItemTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.item = Item.objects.create(name='Test Item', description='Test Desc', category='Test Category', price=10.01, user=self.user)
        self.url = reverse('CreateNewItem', kwargs={'item_id': self.item.id})

    def test_get_single_item(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_single_item_no_auth(self):
        response = self.client.patch(self.url, {'name': 'Updated Name'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_single_item_with_auth(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
