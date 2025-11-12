"""
Unit tests for account settings serializers
Tests validation logic, password verification, and error handling
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'easyfitness_backend.settings')
django.setup()

from django.test import TestCase
from api.models import User
from api.serializers import (
    ChangeUsernameSerializer,
    ChangeEmailSerializer,
    DeleteAccountSerializer,
    hash_password
)


class ChangeUsernameSerializerTest(TestCase):
    """Test ChangeUsernameSerializer validation and password verification"""

    def setUp(self):
        """Create test user"""
        self.user = User.objects.create(
            username='testuser',
            email='test@example.com',
            password_hash=hash_password('TestPass123!')
        )
        self.other_user = User.objects.create(
            username='otheruser',
            email='other@example.com',
            password_hash=hash_password('OtherPass123!')
        )

    def test_valid_username_change(self):
        """Test successful username change with valid data"""
        data = {
            'new_username': 'newusername',
            'current_password': 'TestPass123!'
        }
        serializer = ChangeUsernameSerializer(
            data=data,
            context={'user': self.user}
        )
        self.assertTrue(serializer.is_valid())

    def test_username_with_underscores(self):
        """Test username with underscores is valid"""
        data = {
            'new_username': 'new_user_name',
            'current_password': 'TestPass123!'
        }
        serializer = ChangeUsernameSerializer(
            data=data,
            context={'user': self.user}
        )
        self.assertTrue(serializer.is_valid())

    def test_username_with_numbers(self):
        """Test username with numbers is valid"""
        data = {
            'new_username': 'newuser123',
            'current_password': 'TestPass123!'
        }
        serializer = ChangeUsernameSerializer(
            data=data,
            context={'user': self.user}
        )
        self.assertTrue(serializer.is_valid())

    def test_username_too_short(self):
        """Test username less than 3 characters fails"""
        data = {
            'new_username': 'ab',
            'current_password': 'TestPass123!'
        }
        serializer = ChangeUsernameSerializer(
            data=data,
            context={'user': self.user}
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn('new_username', serializer.errors)

    def test_username_too_long(self):
        """Test username longer than 50 characters fails"""
        data = {
            'new_username': 'a' * 51,
            'current_password': 'TestPass123!'
        }
        serializer = ChangeUsernameSerializer(
            data=data,
            context={'user': self.user}
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn('new_username', serializer.errors)

    def test_username_with_spaces(self):
        """Test username with spaces fails validation"""
        data = {
            'new_username': 'new username',
            'current_password': 'TestPass123!'
        }
        serializer = ChangeUsernameSerializer(
            data=data,
            context={'user': self.user}
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn('new_username', serializer.errors)

    def test_username_with_special_characters(self):
        """Test username with special characters fails validation"""
        data = {
            'new_username': 'new-user!',
            'current_password': 'TestPass123!'
        }
        serializer = ChangeUsernameSerializer(
            data=data,
            context={'user': self.user}
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn('new_username', serializer.errors)

    def test_username_already_taken(self):
        """Test username that is already taken fails"""
        data = {
            'new_username': 'otheruser',  # Already exists
            'current_password': 'TestPass123!'
        }
        serializer = ChangeUsernameSerializer(
            data=data,
            context={'user': self.user}
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn('new_username', serializer.errors)

    def test_incorrect_password(self):
        """Test incorrect password fails validation"""
        data = {
            'new_username': 'validnewname',
            'current_password': 'WrongPassword!'
        }
        serializer = ChangeUsernameSerializer(
            data=data,
            context={'user': self.user}
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn('current_password', serializer.errors)

    def test_same_username_allowed(self):
        """Test changing to same username is allowed (no-op)"""
        data = {
            'new_username': 'testuser',  # Same as current
            'current_password': 'TestPass123!'
        }
        serializer = ChangeUsernameSerializer(
            data=data,
            context={'user': self.user}
        )
        self.assertTrue(serializer.is_valid())

    def tearDown(self):
        """Clean up test users"""
        User.objects.all().delete()


class ChangeEmailSerializerTest(TestCase):
    """Test ChangeEmailSerializer validation and password verification"""

    def setUp(self):
        """Create test user"""
        self.user = User.objects.create(
            username='testuser',
            email='test@example.com',
            password_hash=hash_password('TestPass123!')
        )
        self.other_user = User.objects.create(
            username='otheruser',
            email='other@example.com',
            password_hash=hash_password('OtherPass123!')
        )

    def test_valid_email_change(self):
        """Test successful email change with valid data"""
        data = {
            'new_email': 'newemail@example.com',
            'current_password': 'TestPass123!'
        }
        serializer = ChangeEmailSerializer(
            data=data,
            context={'user': self.user}
        )
        self.assertTrue(serializer.is_valid())

    def test_invalid_email_format(self):
        """Test invalid email format fails validation"""
        data = {
            'new_email': 'notanemail',
            'current_password': 'TestPass123!'
        }
        serializer = ChangeEmailSerializer(
            data=data,
            context={'user': self.user}
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn('new_email', serializer.errors)

    def test_email_already_taken(self):
        """Test email that is already taken fails"""
        data = {
            'new_email': 'other@example.com',  # Already exists
            'current_password': 'TestPass123!'
        }
        serializer = ChangeEmailSerializer(
            data=data,
            context={'user': self.user}
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn('new_email', serializer.errors)

    def test_incorrect_password(self):
        """Test incorrect password fails validation"""
        data = {
            'new_email': 'newemail@example.com',
            'current_password': 'WrongPassword!'
        }
        serializer = ChangeEmailSerializer(
            data=data,
            context={'user': self.user}
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn('current_password', serializer.errors)

    def test_same_email_allowed(self):
        """Test changing to same email is allowed (no-op)"""
        data = {
            'new_email': 'test@example.com',  # Same as current
            'current_password': 'TestPass123!'
        }
        serializer = ChangeEmailSerializer(
            data=data,
            context={'user': self.user}
        )
        self.assertTrue(serializer.is_valid())

    def test_email_case_insensitive(self):
        """Test email validation is case-sensitive (Django default)"""
        data = {
            'new_email': 'NewEmail@Example.com',
            'current_password': 'TestPass123!'
        }
        serializer = ChangeEmailSerializer(
            data=data,
            context={'user': self.user}
        )
        self.assertTrue(serializer.is_valid())

    def tearDown(self):
        """Clean up test users"""
        User.objects.all().delete()


class DeleteAccountSerializerTest(TestCase):
    """Test DeleteAccountSerializer validation and password verification"""

    def setUp(self):
        """Create test user"""
        self.user = User.objects.create(
            username='testuser',
            email='test@example.com',
            password_hash=hash_password('TestPass123!')
        )

    def test_valid_deletion_request(self):
        """Test successful deletion request with valid data"""
        data = {
            'current_password': 'TestPass123!',
            'confirm_deletion': True
        }
        serializer = DeleteAccountSerializer(
            data=data,
            context={'user': self.user}
        )
        self.assertTrue(serializer.is_valid())

    def test_deletion_not_confirmed(self):
        """Test deletion without confirmation fails"""
        data = {
            'current_password': 'TestPass123!',
            'confirm_deletion': False
        }
        serializer = DeleteAccountSerializer(
            data=data,
            context={'user': self.user}
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn('confirm_deletion', serializer.errors)

    def test_incorrect_password(self):
        """Test incorrect password fails validation"""
        data = {
            'current_password': 'WrongPassword!',
            'confirm_deletion': True
        }
        serializer = DeleteAccountSerializer(
            data=data,
            context={'user': self.user}
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn('current_password', serializer.errors)

    def test_missing_password(self):
        """Test missing password field fails validation"""
        data = {
            'confirm_deletion': True
        }
        serializer = DeleteAccountSerializer(
            data=data,
            context={'user': self.user}
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn('current_password', serializer.errors)

    def test_missing_confirmation(self):
        """Test missing confirmation field fails validation"""
        data = {
            'current_password': 'TestPass123!'
        }
        serializer = DeleteAccountSerializer(
            data=data,
            context={'user': self.user}
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn('confirm_deletion', serializer.errors)

    def tearDown(self):
        """Clean up test users"""
        User.objects.all().delete()


if __name__ == '__main__':
    import unittest
    unittest.main()
