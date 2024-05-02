from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.core.files.uploadedfile import SimpleUploadedFile
from ..models import CustomUser, Address

class CustomUserModelTest(TestCase):

    def create_address(self, name="Test Address"):
        return Address.objects.create(
            name=name,
            street="123 Main St",
            zipcode="12345",
            latitude=40.712776,
            longitude=-74.005974
        )

    def create_user(self, username="testuser", email="test@example.com", phone="1234567890", address=None, displayname="Test User", is_visible=True, is_verified=True):
        return CustomUser.objects.create_user(
            username=username,
            email=email,
            phone=phone,
            address=address,
            displayname=displayname,
            is_visible=is_visible,
            is_verified=is_verified
        )

    def test_user_creation(self):
        address = self.create_address()
        user = self.create_user(address=address)
        self.assertTrue(isinstance(user, CustomUser))
        self.assertEqual(user.__str__(), user.username)
        self.assertEqual(user.address, address)
        self.assertEqual(user.displayname, "Test User")

    def test_user_email_uniqueness(self):
        user1 = self.create_user(username="user1", email="unique@example.com")
        with self.assertRaises(IntegrityError):
            user2 = self.create_user(username="user2", email="unique@example.com")
            user2.full_clean()

    def test_user_phone_length(self):
        with self.assertRaises(ValidationError):
            user = self.create_user(phone="12345")
            user.full_clean()


class AddressModelTest(TestCase):

    def create_address(self, name="Default Address"):
        return Address.objects.create(
            name=name,
            street="456 Elm Street",
            zipcode="54321",
            latitude=35.689487,
            longitude=139.691706
        )

    def test_address_creation(self):
        address = self.create_address()
        self.assertTrue(isinstance(address, Address))
        self.assertEqual(address.__str__(), address.name)
        self.assertEqual(address.street, "456 Elm Street")
        self.assertEqual(address.zipcode, "54321")

    def test_address_name_uniqueness(self):
        address1 = self.create_address(name="Unique Address")
        with self.assertRaises(IntegrityError):
            address2 = self.create_address(name="Unique Address")
            address2.full_clean()

    def test_address_coordinates(self):
        address = self.create_address()
        self.assertEqual(address.latitude, 35.689487)
        self.assertEqual(address.longitude, 139.691706)