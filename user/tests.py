from datetime import datetime
from user.models import CustomUser, DateTimeRecord
from django.utils import timezone
from .serializers import (
    CustomUserSerializer,
    CustomUserRegistrationSerializer,
    ChangePasswordSerializer,
)
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework.test import APIClient
from django.urls import reverse
from django.test import TestCase
from unittest.mock import patch


class CustomUserModelTests(TestCase):
    """
    Test cases for the CustomUser model.
    """

    def setUp(self):
        """
        Set up necessary test data before running individual tests.
        """
        self.user_email = "test@example.com"
        CustomUser.objects.create(
            username="testuser",
            email=self.user_email,
            father_name="testfather"
        )

    def test_user_creation(self):
        """
        Test if a user is correctly created with the provided data.
        """
        user = CustomUser.objects.get(email=self.user_email)
        self.assertEqual(user.email, self.user_email)

    def test_email_uniqueness(self):
        """
        Test that creating a user with an email that already exists raises an exception.
        """
        with self.assertRaises(Exception):  # Expecting IntegrityError, but to keep it general
            CustomUser.objects.create(
                username="testuser2",
                email=self.user_email,  # same email as before
                father_name="testfather2"
            )

    def test_custom_save_method(self):
        """
        Test if the custom save method updates the 'last_profile_update' field.
        """
        user = CustomUser.objects.get(email=self.user_email)
        original_last_profile_update = user.last_profile_update
        user.save()  # Call custom save
        updated_user = CustomUser.objects.get(email=self.user_email)
        self.assertNotEqual(original_last_profile_update, updated_user.last_profile_update)

    def test_default_software_engineering_experience(self):
        """
        Test if the default value for the 'software_engineering_experience' field is 0.
        """
        user = CustomUser.objects.get(email=self.user_email)
        self.assertEqual(user.software_engineering_experience, 0)


class DateTimeRecordModelTests(TestCase):
    """
    Test cases for the DateTimeRecord model.
    """

    def test_record_creation(self):
        """
        Test if a DateTimeRecord is correctly created with the provided datetime.
        """
        record_time = timezone.now()
        DateTimeRecord.objects.create(datetime=record_time)
        record = DateTimeRecord.objects.get(datetime=record_time)
        self.assertEqual(record_time, record.datetime)

    def test_default_converted_to_utc(self):
        """
        Test if the 'converted_to_utc' field has its default value set to False.
        """
        record_time = datetime.now()
        DateTimeRecord.objects.create(datetime=record_time)
        record = DateTimeRecord.objects.get(datetime=record_time)
        self.assertEqual(record.converted_to_utc, False)


class CustomUserSerializerTestCase(TestCase):
    """Test case for CustomUserSerializer operations."""

    def setUp(self):
        """Setup test data for CustomUserSerializer tests."""
        self.user_attributes = {
            'username': 'tes343t3user',
            'email': 'test112234@example.com',
            'father_name': 'testfather',
            'description': 'test description',
            'software_engineering_experience': 2,
            'country': 'Algeria'
        }
        self.user = CustomUser.objects.create(**self.user_attributes)
        self.serializer = CustomUserSerializer(instance=self.user)

    def test_successful_serialization(self):
        """Test that a user object serializes correctly."""
        data = self.serializer.data
        self.assertEqual(set(data.keys()),
                         {'id', 'username', 'email', 'father_name', 'description', 'software_engineering_experience',
                          'last_profile_update', 'country'})
        self.assertEqual(data['username'], self.user_attributes['username'])

    def test_successful_deserialization(self):
        """Test that a user object can be deserialized and saved without errors."""
        modified_attributes = self.user_attributes.copy()
        modified_attributes['username'] = 'anotherusername'
        modified_attributes['email'] = 'anotheremail@example.com'

        serializer = CustomUserSerializer(data=modified_attributes)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, modified_attributes['username'])


class CustomUserRegistrationSerializerTestCase(TestCase):
    """Test case for CustomUserRegistrationSerializer operations."""

    def setUp(self):
        """Setup test data for CustomUserRegistrationSerializer tests."""
        self.user_attributes = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'father_name': 'testfather',
            'description': 'test description',
            'software_engineering_experience': 2,
            'country': 'Algeria'
        }

    def test_successful_serialization(self):
        """Test that a user object serializes correctly using the registration serializer."""
        user = CustomUser.objects.create(**self.user_attributes)
        serializer = CustomUserRegistrationSerializer(instance=user)
        self.assertEqual(serializer.data['username'], self.user_attributes['username'])
        user.delete()

    def test_successful_deserialization(self):
        """Test that a user object can be deserialized and saved using the registration serializer."""
        serializer = CustomUserRegistrationSerializer(data=self.user_attributes)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, self.user_attributes['username'])

    def test_password_validation(self):
        """Test that password validation works correctly in the registration serializer."""
        invalid_user_attributes = self.user_attributes.copy()
        invalid_user_attributes['password'] = 'short'
        serializer = CustomUserRegistrationSerializer(data=invalid_user_attributes)
        self.assertFalse(serializer.is_valid())
        self.assertTrue('password' in serializer.errors)


class ChangePasswordSerializerTestCase(TestCase):
    """Test case for ChangePasswordSerializer operations."""

    def setUp(self):
        """Setup test data for ChangePasswordSerializer tests."""
        self.password_attributes = {
            'old_password': 'password123',
            'new_password': 'password456',
        }

    def test_successful_serialization(self):
        """Test that password attributes serialize correctly."""
        serializer = ChangePasswordSerializer(data=self.password_attributes)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['old_password'], self.password_attributes['old_password'])

    def test_password_validation(self):
        """Test that password validation works correctly in the password change serializer."""
        invalid_password_attributes = self.password_attributes.copy()
        invalid_password_attributes['new_password'] = 'short'
        serializer = ChangePasswordSerializer(data=invalid_password_attributes)
        self.assertFalse(serializer.is_valid())
        self.assertTrue('new_password' in serializer.errors)


class UserViewTests(TestCase):
    def setUp(self):
        """
        Create a test user and log them in.
        """
        self.user_data = {
            'username': 'testuser',
            'password': 'testpass123',
            'email': 'testuser@example.com',
            'father_name': 'testfather',
            'description': 'Test description',
            'country': 'Algeria'
        }
        self.user = get_user_model().objects.create_user(**self.user_data)
        self.client.login(email=self.user_data['email'], password=self.user_data['password'])

    def test_logout_view(self):
        """
        Send GET request to the logout view and check if the user is logged out
        and redirected to login page.
        """
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_edit_profile_get(self):
        """
        Send GET request to the edit profile view and check if the edit form is displayed.
        """
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/edit_profile.html')

    def test_edit_profile_post(self):
        """
        Send POST request to the edit profile view, update user details,
        and check if the user is redirected to the home page after the update.
        """
        response = self.client.post(reverse('edit_profile'), {
            'username': 'updateduser',
            'email': 'updateduser@example.com',
            'father_name': 'updatedfather',
            'description': 'Updated description',
            'country': 'Updated Country'
        })

        updated_user = get_user_model().objects.get(pk=self.user.pk)

        self.assertEqual(updated_user.username, 'updateduser')
        self.assertEqual(updated_user.email, 'updateduser@example.com')
        self.assertEqual(updated_user.father_name, 'updatedfather')
        self.assertEqual(updated_user.description, 'Updated description')
        self.assertEqual(updated_user.country, 'Updated Country')
        self.assertRedirects(response, reverse('home'))


class UserAuthAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.signup_url = reverse('signup-api')
        self.login_url = reverse('login-api')

        # Create a test user
        self.test_username = "testuser"
        self.test_email = "testuser@example.com"
        self.test_password = "securepassword123"
        self.father_name = "John Doe"
        self.description = "Test description"
        self.software_engineering_experience = 5
        self.country = "Algeria"

        self.user = CustomUser.objects.create_user(
            username=self.test_username,
            email=self.test_email,
            password=self.test_password,
            father_name=self.father_name,
            description=self.description,
            software_engineering_experience=self.software_engineering_experience,
            country=self.country
        )

    def test_signup_api(self):
        # Use this data to create a new user
        data = {
            'username': 'test1user',
            'email': 'test135323@example.com',
            'password': 'password123',
            'father_name': 'John Doe',
            'description': 'Just a test user.',
            'software_engineering_experience': 2,
            'country': 'Algeria'
        }

        response = self.client.post(reverse('signup-api'), data)

        # Debugging statements
        print("Signup API Response:", response.data)
        print("Signup API Status Code:", response.status_code)

        # Assertions
        self.assertEqual(response.status_code, 201)  # Expecting a CREATED status code
        self.assertIn('username', response.data)
        self.assertNotIn('password', response.data)  # Password should not be serialized

    @patch('rest_framework_simplejwt.tokens.RefreshToken.for_user')
    def test_login_api(self, mock_for_user):
        # Mock JWT token return

        response = self.client.post(self.login_url, data={
            'email': self.test_email,
            'password': self.test_password,
        })

        # Debugging statements
        print("Login API Response:", response.data)
        print("Login API Status Code:", response.status_code)

        # Assertions
        self.assertEqual(response.status_code, 200)  # Expecting an OK status code
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)


class ChangePasswordAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.change_password_url = reverse('change-password-api')

        self.user_data = {
            'username': 'test1user',
            'email': 'test135323@example.com',
            'password': 'password123',
            'father_name': 'John Doe',
            'description': 'Just a test user.',
            'software_engineering_experience': 2,
            'country': 'Algeria'
        }

        self.user = CustomUser.objects.create_user(**self.user_data)
        self.client.force_authenticate(user=self.user)  # Logging in the user

    def test_successful_password_change(self):
        data = {
            'old_password': self.user_data['password'],
            'new_password': 'newsecurepassword123'
        }

        response = self.client.put(self.change_password_url, data)

        # Ensure the response indicates success
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['detail'], "Password updated successfully")

        # Try to authenticate with the new password to ensure the password has changed
        user = authenticate(email=self.user_data['email'], password=data['new_password'])
        self.assertIsNotNone(user)

    def test_failure_with_incorrect_old_password(self):
        data = {
            'old_password': 'incorrectpassword',
            'new_password': 'newsecurepassword123'
        }

        response = self.client.put(self.change_password_url, data)

        # Ensure the response indicates an error
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['old_password'][0], "Wrong password.")

        # Ensure the user's password hasn't changed
        user = authenticate(email=self.user_data['email'], password=self.user_data['password'])
        self.assertIsNotNone(user)
