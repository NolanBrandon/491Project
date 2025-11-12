"""
Mock unit tests for account settings serializers
Tests validation logic without requiring database connection
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os
import django

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'easyfitness_backend.settings')
django.setup()


class MockUser:
    """Mock User model for testing"""
    def __init__(self, id, username, email, password_hash):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash


class ChangeUsernameSerializerMockTest(unittest.TestCase):
    """Test ChangeUsernameSerializer validation with mocked dependencies"""

    def setUp(self):
        """Set up test fixtures"""
        self.user = MockUser(
            id='123',
            username='testuser',
            email='test@example.com',
            password_hash='pbkdf2_sha256$600000$mocksalt$mockhash'
        )

    @patch('api.serializers.User')
    @patch('api.serializers.verify_password')
    def test_valid_username_change(self, mock_verify_password, mock_user_model):
        """Test successful username change with valid data"""
        # Setup mocks
        mock_verify_password.return_value = True
        mock_user_model.objects.filter.return_value.exclude.return_value.exists.return_value = False

        from api.serializers import ChangeUsernameSerializer

        data = {
            'new_username': 'newusername',
            'current_password': 'TestPass123!'
        }
        serializer = ChangeUsernameSerializer(
            data=data,
            context={'user': self.user}
        )

        # Should be valid
        is_valid = serializer.is_valid()
        self.assertTrue(is_valid, f"Serializer errors: {serializer.errors}")

    @patch('api.serializers.User')
    @patch('api.serializers.verify_password')
    def test_username_with_underscores(self, mock_verify_password, mock_user_model):
        """Test username with underscores is valid"""
        mock_verify_password.return_value = True
        mock_user_model.objects.filter.return_value.exclude.return_value.exists.return_value = False

        from api.serializers import ChangeUsernameSerializer

        data = {
            'new_username': 'new_user_name',
            'current_password': 'TestPass123!'
        }
        serializer = ChangeUsernameSerializer(
            data=data,
            context={'user': self.user}
        )
        self.assertTrue(serializer.is_valid())

    @patch('api.serializers.User')
    @patch('api.serializers.verify_password')
    def test_username_with_numbers(self, mock_verify_password, mock_user_model):
        """Test username with numbers is valid"""
        mock_verify_password.return_value = True
        mock_user_model.objects.filter.return_value.exclude.return_value.exists.return_value = False

        from api.serializers import ChangeUsernameSerializer

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
        from api.serializers import ChangeUsernameSerializer

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
        from api.serializers import ChangeUsernameSerializer

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
        from api.serializers import ChangeUsernameSerializer

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
        from api.serializers import ChangeUsernameSerializer

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

    @patch('api.serializers.User')
    @patch('api.serializers.verify_password')
    def test_username_already_taken(self, mock_verify_password, mock_user_model):
        """Test username that is already taken fails"""
        mock_verify_password.return_value = True
        mock_user_model.objects.filter.return_value.exclude.return_value.exists.return_value = True

        from api.serializers import ChangeUsernameSerializer

        data = {
            'new_username': 'existinguser',
            'current_password': 'TestPass123!'
        }
        serializer = ChangeUsernameSerializer(
            data=data,
            context={'user': self.user}
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn('new_username', serializer.errors)

    @patch('api.serializers.User')
    @patch('api.serializers.verify_password')
    def test_incorrect_password(self, mock_verify_password, mock_user_model):
        """Test incorrect password fails validation"""
        mock_verify_password.return_value = False
        mock_user_model.objects.filter.return_value.exclude.return_value.exists.return_value = False

        from api.serializers import ChangeUsernameSerializer

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


class ChangeEmailSerializerMockTest(unittest.TestCase):
    """Test ChangeEmailSerializer validation with mocked dependencies"""

    def setUp(self):
        """Set up test fixtures"""
        self.user = MockUser(
            id='123',
            username='testuser',
            email='test@example.com',
            password_hash='pbkdf2_sha256$600000$mocksalt$mockhash'
        )

    @patch('api.serializers.User')
    @patch('api.serializers.verify_password')
    def test_valid_email_change(self, mock_verify_password, mock_user_model):
        """Test successful email change with valid data"""
        mock_verify_password.return_value = True
        mock_user_model.objects.filter.return_value.exclude.return_value.exists.return_value = False

        from api.serializers import ChangeEmailSerializer

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
        from api.serializers import ChangeEmailSerializer

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

    @patch('api.serializers.User')
    @patch('api.serializers.verify_password')
    def test_email_already_taken(self, mock_verify_password, mock_user_model):
        """Test email that is already taken fails"""
        mock_verify_password.return_value = True
        mock_user_model.objects.filter.return_value.exclude.return_value.exists.return_value = True

        from api.serializers import ChangeEmailSerializer

        data = {
            'new_email': 'existing@example.com',
            'current_password': 'TestPass123!'
        }
        serializer = ChangeEmailSerializer(
            data=data,
            context={'user': self.user}
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn('new_email', serializer.errors)

    @patch('api.serializers.User')
    @patch('api.serializers.verify_password')
    def test_incorrect_password(self, mock_verify_password, mock_user_model):
        """Test incorrect password fails validation"""
        mock_verify_password.return_value = False
        mock_user_model.objects.filter.return_value.exclude.return_value.exists.return_value = False

        from api.serializers import ChangeEmailSerializer

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


class DeleteAccountSerializerMockTest(unittest.TestCase):
    """Test DeleteAccountSerializer validation with mocked dependencies"""

    def setUp(self):
        """Set up test fixtures"""
        self.user = MockUser(
            id='123',
            username='testuser',
            email='test@example.com',
            password_hash='pbkdf2_sha256$600000$mocksalt$mockhash'
        )

    @patch('api.serializers.verify_password')
    def test_valid_deletion_request(self, mock_verify_password):
        """Test successful deletion request with valid data"""
        mock_verify_password.return_value = True

        from api.serializers import DeleteAccountSerializer

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
        from api.serializers import DeleteAccountSerializer

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

    @patch('api.serializers.verify_password')
    def test_incorrect_password(self, mock_verify_password):
        """Test incorrect password fails validation"""
        mock_verify_password.return_value = False

        from api.serializers import DeleteAccountSerializer

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
        from api.serializers import DeleteAccountSerializer

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
        from api.serializers import DeleteAccountSerializer

        data = {
            'current_password': 'TestPass123!'
        }
        serializer = DeleteAccountSerializer(
            data=data,
            context={'user': self.user}
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn('confirm_deletion', serializer.errors)


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)
