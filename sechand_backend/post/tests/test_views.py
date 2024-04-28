from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from post.models import Item, UserCollection
from user.models import Address, CustomUser
from rest_framework import status
from rest_framework.test import APIClient
from decimal import Decimal

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

class CreateNewItemsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.url = reverse('CreateNewItem')

    # def test_create_new_item(self):
    #     self.client.force_authenticate(user=self.user)
    #     item_data = {'name': 'Test Item2', 'description':'A description', 'category':'Test category', 'price':11.01, 'seller': '1'}
    #     response = self.client.post(self.url, item_data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class ProcessSingleItemTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.address = Address.objects.create(name='Test Address', street='123 Main St', zipcode='12345', latitude=Decimal('40.7128'), longitude=Decimal('-74.0060'))
        self.user.address = self.address
        self.item = Item.objects.create(name='Test Item', description='Test Desc', category='Test Category', price=10.01, seller=self.user)
        self.url = reverse('ProcessSingleItem', kwargs={'item_id': self.item.id})
        self.update_url = reverse('ProcessSingleItem', kwargs={'item_id': self.item.id})
        self.non_url = reverse('ProcessSingleItem', kwargs={'item_id': '12345678-1234-5678-1234-567812345678'})


    def test_get_single_item(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_not_exist_item(self):
        response = self.client.get(self.non_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # def test_patch_non_exist_with_no_auth(self):
    #     response = self.client.patch(self.url, {'price': 25.00})
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_single_item_with_auth(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.url, {'price': 25.00})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_patch_non_exist_with_auth(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.non_url, {'price': 25.00})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    # def test_patch_bad_data_with_auth(self):
    #     self.client.force_authenticate(user=self.user)
    #     response = self.client.patch(self.url, {'gate': 25.00})
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_single_item_with_auth(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SearchItemsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('SearchItems')
        # Set up user and address
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.address = Address.objects.create(name='Test Address', street='123 Main St', zipcode='12345', latitude=Decimal('40.7128'), longitude=Decimal('-74.0060'))
        self.user.address = self.address
        self.user.save()

        self.item1 = Item.objects.create(
            name='Math Textbook',
            description='Description for Item 1',
            category='Books',
            price=Decimal('20.00'),
            seller=self.user,
            is_sold=False
        )
        self.item2 = Item.objects.create(
            name='Baseball',
            description='Description for Item 2',
            category='Sporting Goods',
            price=Decimal('50.00'),
            seller=self.user,
            is_sold=False
        )
        
    def test_search_items_with_description(self):
        response = self.client.get(reverse('GetAllItems'))
        self.assertEqual(len(response.json()), 2)
        params = {'desc_text': 'Baseball', 'category': 'all'}
        response = self.client.post(self.url, data=params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        
    def test_search_items_by_price_range(self):
        params = {'desc_text': '', 'lowest_price': '5', 'highest_price': '15', 'category': 'all'}
        response = self.client.post(self.url, data=params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)
        params = {'desc_text': '', 'lowest_price': '5', 'highest_price': '25', 'category': 'all'}
        response = self.client.post(self.url, data=params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        
        
    def test_search_items_by_category(self):
        params = {'desc_text': '', 'category': 'Books', 'location': [], 'distance': '-1'}
        response = self.client.post(self.url, data=params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class AddNewCollectionTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Set up user and address
        self.seller = User.objects.create_user(username='testseller', password='seller1234', email='testseller@test.com')
        self.buyer = User.objects.create_user(username='testbuyer', password='buyer1234', email='testbuyer@test.com')
        self.item = Item.objects.create(
            name='Math Textbook',
            description='Description for Item 1',
            category='Books',
            price=Decimal('20.00'),
            seller=self.seller,
            is_sold=False
        )
        self.url = reverse('AddNewCollection', kwargs={'item_id': str(self.item.id)})
    
    def test_add_collection(self):
        self.client.force_authenticate(user=self.buyer)
        # params = {'user': self.user.id, 'item': self.item1.id}
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class GetCollectionTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Set up user and address
        self.seller = User.objects.create_user(username='testseller', password='seller1234', email='testseller@test.com')
        self.buyer = User.objects.create_user(username='testbuyer', password='buyer1234', email='testbuyer@test.com')
        self.address = Address.objects.create(name='Test Address', street='123 Main St', zipcode='12345', latitude=Decimal('40.7128'), longitude=Decimal('-74.0060'))
        self.seller.address = self.address
        self.buyer.address = self.address
        self.item = Item.objects.create(
            name='Baseball',
            description='Description for Item 2',
            category='Sporting Goods',
            price=Decimal('50.00'),
            seller=self.seller,
            is_sold=False
        )
        self.item2 = Item.objects.create(
            name='Math Textbook',
            description='Description for Item 1',
            category='Books',
            price=Decimal('20.00'),
            seller=self.seller,
            is_sold=False
        )
        self.collection = UserCollection.objects.create(
            user = self.buyer,
            item = self.item.id
        )

        self.url = reverse('GetUserCollection')
        self.isCollectUrl = reverse('IsUserCollected', kwargs={'item_id': str(self.item.id)})
    
    def test_get_collection(self):
        self.client.force_authenticate(user=self.buyer)
        # params = {'user': self.user.id, 'item': self.item1.id}
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['id'], str(self.item.id))
        self.assertEqual(response.json()[0]['name'], self.item.name)
        self.assertEqual(response.json()[0]['description'], self.item.description)
        self.assertEqual(response.json()[0]['category'], self.item.category)

        self.collection2 = UserCollection.objects.create(
            user = self.buyer,
            item = self.item2.id
        )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[1]['id'], str(self.item.id))
        self.assertEqual(response.json()[1]['name'], self.item.name)
        self.assertEqual(response.json()[1]['description'], self.item.description)
        self.assertEqual(response.json()[1]['category'], self.item.category)

    def test_is_collected(self):
        self.client.force_authenticate(user=self.buyer)
        response = self.client.post(self.isCollectUrl)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['collected'], True)

class DeleteCollectionTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Set up user and address
        self.seller = User.objects.create_user(username='testseller', password='seller1234', email='testseller@test.com')
        self.buyer = User.objects.create_user(username='testbuyer', password='buyer1234', email='testbuyer@test.com')

        self.item = Item.objects.create(
            name='Baseball',
            description='Description for Item 2',
            category='Sporting Goods',
            price=Decimal('50.00'),
            seller=self.seller,
            is_sold=False
        )
        self.item2 = Item.objects.create(
            name='Math Textbook',
            description='Description for Item 1',
            category='Books',
            price=Decimal('20.00'),
            seller=self.seller,
            is_sold=False
        )
        self.collection = UserCollection.objects.create(
            user = self.buyer,
            item = self.item.id
        )
        self.collection2 = UserCollection.objects.create(
            user = self.buyer,
            item = self.item2.id
        )

        self.addurl = reverse('AddNewCollection', kwargs={'item_id': str(self.item2.id)})
        self.delurl = reverse('DeleteUserCollection', kwargs={'item_id': str(self.item2.id)})

        self.client.post(self.addurl)
    
    def test_delete_collection(self):
        self.client.force_authenticate(user=self.buyer)
        # params = {'user': self.user.id, 'item': self.item1.id}
        response = self.client.delete(self.delurl)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()['message'], "UserCollection deleted")

        response = self.client.delete(self.delurl)
        # self.assertRaises(UserCollection.DoesNotExist, self.client.delete, self.delurl)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['error'], "UserCollection not found")

class TransactionTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Set up user and address
        self.seller = User.objects.create_user(username='testseller', password='seller1234', email='testseller@test.com')
        self.buyer = User.objects.create_user(username='testbuyer', password='buyer1234', email='testbuyer@test.com')
        self.item = Item.objects.create(
            name='Math Textbook',
            description='Description for Item 1',
            category='Books',
            price=Decimal('20.00'),
            seller=self.seller,
            is_sold=False
        )
        self.url = reverse('SaveTransaction')
        self.getUrl = reverse('GetAllTransactions')
        self.client.force_authenticate(user=self.buyer)
    
    def test_save_transaction(self):
        params = {'item_id': self.item.id, 'seller_id': self.seller.id, 'buyer_id': self.buyer.id, 'price': self.item.price}
        response = self.client.post(self.url, data=params)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_get_transaction(self):
        params = {'item_id': self.item.id, 'seller_id': self.seller.id, 'buyer_id': self.buyer.id, 'price': self.item.price}
        response = self.client.post(self.url, data=params)

        response = self.client.get(self.getUrl)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['name'], 'Math Textbook')

