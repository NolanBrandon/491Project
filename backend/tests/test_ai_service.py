import os
import sys
import django
from django.test import TestCase
from unittest.mock import patch, MagicMock

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'easyfitness_backend.settings')
django.setup()

from api.services import GeminiAIService


class TestGeminiAIService(TestCase):
    """Test cases for the GeminiAIService class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.ai_service = None
    
    def test_service_initialization_success(self):
        """Test that the AI service initializes successfully with valid API key."""
        try:
            self.ai_service = GeminiAIService()
            self.assertIsNotNone(self.ai_service.client)
            self.assertIsNotNone(self.ai_service.api_key)
            self.assertEqual(self.ai_service.model_id, "gemini-2.5-flash")
            print("✅ AI Service initialization test passed")
        except Exception as e:
            self.fail(f"AI Service initialization failed: {e}")
    
    def test_service_initialization_no_api_key(self):
        """Test that the AI service fails gracefully without API key."""
        with patch('api.services.ai_service.config') as mock_config:
            mock_config.side_effect = Exception("GEMINI_API_KEY not found")
            
            with self.assertRaises(Exception):
                GeminiAIService()
            print("✅ No API key handling test passed")
    
    def test_connection_success(self):
        """Test that the connection test works with a real API call."""
        try:
            self.ai_service = GeminiAIService()
            success, response = self.ai_service.test_connection()
            
            self.assertTrue(success)
            self.assertIsNotNone(response)
            self.assertIsInstance(response, str)
            self.assertGreater(len(response), 0)
            print(f"✅ Connection test passed. AI Response: {response[:100]}...")
        except Exception as e:
            self.fail(f"Connection test failed: {e}")
    
    @patch('api.services.ai_service.genai.Client')
    def test_connection_failure(self, mock_client_class):
        """Test that connection failures are handled properly."""
        # Mock the client to raise an exception
        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = Exception("API Error")
        mock_client_class.return_value = mock_client
        
        try:
            ai_service = GeminiAIService()
            success, error_msg = ai_service.test_connection()
            
            self.assertFalse(success)
            self.assertIn("API Error", error_msg)
            print("✅ Connection failure handling test passed")
        except Exception as e:
            self.fail(f"Connection failure test failed: {e}")


def run_manual_test():
    """
    Manual test function that can be run directly.
    Useful for quick testing during development.
    """
    print("🧪 Running manual AI service connection test...")
    print("-" * 60)
    
    try:
        # Test initialization
        print("1. Testing AI service initialization...")
        ai_service = GeminiAIService()
        print("   ✅ Service initialized successfully")
        
        # Test connection
        print("2. Testing AI connection...")
        success, response = ai_service.test_connection()
        
        if success:
            print("   ✅ Connection successful!")
            print(f"   📝 AI Response: {response}")
        else:
            print("   ❌ Connection failed!")
            print(f"   📝 Error: {response}")
            
    except Exception as e:
        print(f"   ❌ Test failed with error: {e}")
    
    print("-" * 60)
    print("🏁 Manual test completed")


if __name__ == "__main__":
    # Run manual test when executed directly
    run_manual_test()