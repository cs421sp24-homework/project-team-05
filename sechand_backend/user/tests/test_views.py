# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase
# from django.contrib.auth import get_user_model
# from django.utils import timezone
# from datetime import timedelta
# import uuid
# from ..models import CustomUser, Address, VerifyEmailCode, ResetPasswordCode
# from ..serializers import CustomUserSerializer

# UserModel = get_user_model()

# class CustomLoginTests(APITestCase):

#     def setUp(self):
#         self.verified_user = UserModel.objects.create_user(username='testuser1', password='testpassword1', email='test1@example.com', is_verified=True)
#         self.unverified_user = UserModel.objects.create_user(username='testuser2', password='testpassword2', email='test2@example.com', is_verified=False)
#         self.login_url = reverse('custom_login')  # Use the actual name of your login url

#     def test_login_success(self):
#         data = {'username': 'testuser1', 'password': 'testpassword1'}
#         response = self.client.post(self.login_url, data, format='json')
#         json_response = response.json()
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertTrue(json_response['registered'])
#         self.assertTrue(json_response['success'])

#     def test_login_unverified_user(self):
#         data = {'username': 'testuser2', 'password': 'testpassword2'}
#         response = self.client.post(self.login_url, data, format='json')
#         json_response = response.json()
#         self.assertTrue(json_response['registered'])
#         self.assertFalse(json_response['success'])
#         self.assertIsNone(json_response['userInfo'])

#     def test_login_incorrect_password(self):
#         data = {'username': 'testuser1', 'password': 'wrongpassword'}
#         response = self.client.post(self.login_url, data, format='json')
#         json_response = response.json()
#         self.assertTrue(json_response['registered'])
#         self.assertFalse(json_response['success'])

#     def test_login_nonexistent_user(self):
#         data = {'username': 'nonexistent', 'password': 'testpassword123'}
#         response = self.client.post(self.login_url, data, format='json')
#         json_response = response.json()
#         self.assertFalse(json_response['registered'])
#         self.assertFalse(json_response['success'])


# class RegisterViewTests(APITestCase):

#     @classmethod
#     def setUpTestData(cls):
#         # Create a test address if your user registration depends on it
#         cls.test_address = Address.objects.create(
#             name='Test Address',
#             street='123 Test St',
#             zipcode='12345',
#             latitude=40.7128,
#             longitude=-74.0060
#         )

#     def setUp(self):
#         # Set up the URL for making requests
#         self.register_url = reverse('register')  # Make sure 'register' is the correct name of your URL in urls.py
#         self.user_data = {
#             'username': 'newuser',
#             'password': 'newpassword123',
#             'email': 'newuser@example.com',
#             'phone': '1234567890',
#             'displayname': 'New User',
#             'address': self.test_address.name,  # Assuming this is the name field of your Address model
#             'image': None,  # Adjust this based on your actual handling of images
#             'is_visible': True
#         }

#     def test_register_new_user(self):
#         response = self.client.post(self.register_url, self.user_data, format='json')
#         json_response = response.json()

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertTrue(json_response.get('new_user'))
#         self.assertIsNotNone(json_response.get('user'))

#     def test_register_existing_user_not_verified(self):
#         # First, create a user that's not verified
#         CustomUser.objects.create_user(
#             username='existinguser',
#             email='existinguser@example.com',
#             password='password123',
#             is_verified=False
#         )

#         # Attempt to register again with the same username
#         self.user_data['username'] = 'existinguser'
#         self.user_data['email'] = 'existinguser@example.com'
#         response = self.client.post(self.register_url, self.user_data, format='json')
#         json_response = response.json()

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertTrue(json_response.get('new_user'))

#     def test_register_existing_user_verified(self):
#         # First, create a user that's already verified
#         CustomUser.objects.create_user(
#             username='verifieduser',
#             email='verifieduser@example.com',
#             password='password123',
#             is_verified=True
#         )

#         # Attempt to register again with the same username
#         self.user_data['username'] = 'verifieduser'
#         self.user_data['email'] = 'verifieduser@example.com'
#         response = self.client.post(self.register_url, self.user_data, format='json')
#         json_response = response.json()

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertFalse(json_response.get('new_user'))


# class VerifyEmailTests(APITestCase):

#     @classmethod
#     def setUpTestData(cls):
#         # Create an unverified user
#         cls.unverified_user = CustomUser.objects.create_user(
#             username='unverifieduser', 
#             email='unverified@example.com', 
#             password='testpassword123', 
#             is_verified=False
#         )
#         # Create a verified user
#         cls.verified_user = CustomUser.objects.create_user(
#             username='verifieduser', 
#             email='verified@example.com', 
#             password='testpassword123', 
#             is_verified=True
#         )
#         # Create a verification code for the unverified user
#         cls.verification_code = VerifyEmailCode.objects.create(
#             user=cls.unverified_user, 
#             code='123456'
#         )

#     def setUp(self):
#         self.verify_email_url = lambda uid: reverse('verify_email', kwargs={'uid': uid})

#     def test_verify_email_success(self):
#         url = self.verify_email_url(self.unverified_user.pk)
#         response = self.client.post(url, {'code': '123456'}, format='json')
#         json_response = response.json()

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertFalse(json_response['expired'])
#         self.assertTrue(json_response['correct'])

#     def test_verify_email_incorrect_code(self):
#         url = self.verify_email_url(self.unverified_user.pk)
#         response = self.client.post(url, {'code': 'wrongcode'}, format='json')
#         json_response = response.json()

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertFalse(json_response['expired'])
#         self.assertFalse(json_response['correct'])

#     def test_verify_email_expired_code(self):
#         # Manually set the verification code to be expired
#         self.verification_code.created_at = timezone.now() - timedelta(minutes=11)  # Make it expired by setting it 11 minutes back
#         self.verification_code.save()

#         url = self.verify_email_url(self.unverified_user.pk)
#         response = self.client.post(url, {'code': '123456'}, format='json')
#         json_response = response.json()

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertTrue(json_response['expired'])
#         self.assertTrue(json_response['correct'])

#     def test_verify_email_already_verified(self):
#         url = self.verify_email_url(self.verified_user.pk)
#         response = self.client.post(url, {'code': 'anycode'}, format='json')
#         json_response = response.json()

#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn('message', json_response)
#         self.assertEqual(json_response['message'], 'Email already verified.')

#     def test_verify_email_invalid_user(self):
#         # Using an arbitrary user ID that doesn't exist
#         url = self.verify_email_url(9999)
#         response = self.client.post(url, {'code': '123456'}, format='json')
#         json_response = response.json()

#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertIn('message', json_response)
#         self.assertEqual(json_response['message'], 'Invalid user.')


# class ResetPasswordTests(APITestCase):

#     @classmethod
#     def setUpTestData(cls):
#         # Create a test user
#         cls.user = CustomUser.objects.create_user(
#             username='testuser', 
#             email='test@example.com', 
#             password='oldpassword123', 
#             is_verified=True
#         )
#         # Create a reset password code for the test user
#         cls.reset_code = ResetPasswordCode.objects.create(
#             user=cls.user, 
#             code='123456',
#             token=uuid.uuid4()
#         )

#     def setUp(self):
#         self.reset_password_url = lambda username: reverse('reset_password', kwargs={'jhed': username})

#     def test_reset_password_success(self):
#         url = self.reset_password_url(self.user.username)
#         data = {'code': '123456', 'new_password': 'newpassword123'}
#         response = self.client.post(url, data, format='json')
#         json_response = response.json()

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertFalse(json_response['expired'])
#         self.assertTrue(json_response['correct'])
#         self.user.refresh_from_db()
#         self.assertTrue(self.user.check_password('newpassword123'))

#     def test_reset_password_incorrect_code(self):
#         url = self.reset_password_url(self.user.username)
#         data = {'code': 'wrongcode', 'new_password': 'newpassword123'}
#         response = self.client.post(url, data, format='json')
#         json_response = response.json()

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertFalse(json_response['expired'])
#         self.assertFalse(json_response['correct'])

#     def test_reset_password_expired_code(self):
#         # Manually set the reset code to be expired
#         self.reset_code.created_at = timezone.now() - timedelta(minutes=11)
#         self.reset_code.save()

#         url = self.reset_password_url(self.user.username)
#         data = {'code': '123456', 'new_password': 'newpassword123'}
#         response = self.client.post(url, data, format='json')
#         json_response = response.json()

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertTrue(json_response['expired'])
#         self.assertTrue(json_response['correct'])

#     def test_reset_password_invalid_user(self):
#         # Using an arbitrary username that doesn't exist
#         url = self.reset_password_url('nonexistentuser')
#         data = {'code': '123456', 'new_password': 'newpassword123'}
#         response = self.client.post(url, data, format='json')
#         json_response = response.json()

#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertIn('message', json_response)
#         self.assertEqual(json_response['message'], 'Invalid user.')


# class UserProfileTests(APITestCase):

#     @classmethod
#     def setUpTestData(cls):
#         # Create a test user and test address
#         cls.user = CustomUser.objects.create_user(
#             username='testuser',
#             email='test@example.com',
#             password='testpassword123',
#             displayname='Test User',
#             phone='1234567890',
#             is_visible=True
#         )
#         cls.address = Address.objects.create(
#             name='Test Address',
#             street='123 Test St',
#             zipcode='12345',
#             latitude='40.7128',
#             longitude='-74.0060'
#         )

#     def setUp(self):
#         # Authenticate the test client with the test user
#         self.client.force_authenticate(user=self.user)

#     def test_get_user_profile(self):
#         # Define the URL for the get_user_profile view
#         url = reverse('get_user_profile')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
        
#         # Check that the response contains the correct user data
#         serializer = CustomUserSerializer(self.user)
#         self.assertEqual(response.json(), serializer.data)

#     def test_update_user_profile(self):
#         # Define the URL for the update_user_profile view
#         url = reverse('update_user_profile')
#         data = {
#             'displayname': 'New Display Name',
#             'address': self.address.name,
#             'phone': '0987654321',
#             'is_visible': False
#         }
#         response = self.client.patch(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
        
#         # Check that the user's data was updated correctly
#         self.user.refresh_from_db()  # Reload the user from the database
#         self.assertEqual(self.user.displayname, 'New Display Name')
#         self.assertEqual(self.user.address, self.address)
#         self.assertEqual(self.user.phone, '0987654321')
#         self.assertFalse(self.user.is_visible)

#     def test_update_user_profile_with_invalid_address(self):
#         # Test updating the user's profile with a non-existent address
#         url = reverse('update_user_profile')
#         data = {
#             'displayname': 'Another Display Name',
#             'address': 'Nonexistent Address',
#             'phone': '0987654321',
#             'is_visible': False
#         }
#         response = self.client.patch(url, data, format='json')
#         # Expecting failure due to invalid address
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)