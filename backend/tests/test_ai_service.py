import os
import sys
import django
import json
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

    @patch('api.services.ai_service.genai.configure')
    @patch('api.services.ai_service.genai.GenerativeModel')
    def test_service_initialization_success(self, mock_generative_model, mock_configure):
        """Test that the AI service initializes successfully with valid API key."""
        self.ai_service = GeminiAIService()
        mock_configure.assert_called_once()
        mock_generative_model.assert_called_once_with("gemini-2.5-flash")
        self.assertIsNotNone(self.ai_service.model)
        self.assertIsNotNone(self.ai_service.api_key)
        self.assertEqual(self.ai_service.model_id, "gemini-2.5-flash")
        print("✅ AI Service initialization test passed")
    
    def test_service_initialization_no_api_key(self):
        """Test that the AI service fails gracefully without API key."""
        with patch('api.services.ai_service.config') as mock_config:
            mock_config.side_effect = Exception("GEMINI_API_KEY not found")
            
            with self.assertRaises(Exception):
                GeminiAIService()
            print("✅ No API key handling test passed")
    
    @patch('api.services.ai_service.genai.GenerativeModel')
    def test_exercise_plan_generation(self, mock_generative_model):
        """Test that the exercise plan generation works with mocked data."""
        # Setup mock
        mock_response = MagicMock()
        mock_response.text = json.dumps({
            "plan_name": "Mock Muscle Plan",
            "plan_description": "A mocked plan for testing.",
            "days": [{"day_number": 1, "day_name": "Test Day", "exercises": [{"exercise_name": "Mock Lifts", "sets": 3, "reps": "10"}]}]
        })
        mock_model_instance = MagicMock()
        mock_model_instance.generate_content.return_value = mock_response
        mock_generative_model.return_value = mock_model_instance

        self.ai_service = GeminiAIService()
        
        result = self.ai_service.generate_exercise_plan("build muscle", "intermediate", 4, {"age": 25, "gender": "male"})
        
        self.assertTrue(result['success'])
        self.assertEqual(result['data']['plan_name'], "Mock Muscle Plan")
        mock_model_instance.generate_content.assert_called_once()
        _args, call_kwargs = mock_model_instance.generate_content.call_args
        self.assertIn('generation_config', call_kwargs)
        self.assertEqual(call_kwargs['generation_config'].response_mime_type, "application/json")
        print("✅ Mocked exercise plan generation test passed")

    @patch('api.services.ai_service.genai.GenerativeModel')
    def test_meal_plan_generation(self, mock_generative_model):
        """Test that the meal plan generation works with mocked data."""
        # Setup mock
        mock_response = MagicMock()
        mock_response.text = json.dumps({
            "plan_name": "Mock Meal Plan",
            "plan_description": "A mocked meal plan.",
            "days": [{"day_number": 1, "meals": {}, "daily_totals": {}}]
        })
        mock_model_instance = MagicMock()
        mock_model_instance.generate_content.return_value = mock_response
        mock_generative_model.return_value = mock_model_instance

        self.ai_service = GeminiAIService()

        result = self.ai_service.generate_meal_plan("lose weight", 1800, ["vegetarian"], {"age": 30, "gender": "female"})

        self.assertTrue(result['success'])
        self.assertEqual(result['data']['plan_name'], "Mock Meal Plan")
        mock_model_instance.generate_content.assert_called_once()
        _args, call_kwargs = mock_model_instance.generate_content.call_args
        self.assertIn('generation_config', call_kwargs)
        self.assertEqual(call_kwargs['generation_config'].response_mime_type, "application/json")
        print("✅ Mocked meal plan generation test passed")
    
    @patch('api.services.ai_service.genai.GenerativeModel')
    def test_connection_failure(self, mock_generative_model):
        """Test that connection failures are handled properly."""
        # Mock the client to raise an exception
        mock_model_instance = MagicMock()
        mock_model_instance.generate_content.side_effect = Exception("API Error")
        mock_generative_model.return_value = mock_model_instance
        
        ai_service = GeminiAIService()
        success, error_msg = ai_service.test_connection()
        
        self.assertFalse(success)
        self.assertIn("API Error", error_msg)
        print("✅ Connection failure handling test passed")


def run_manual_test():
    """
    Manual test function that can be run directly to hit the live AI API.
    Useful for quick testing during development.
    """
    print("🧪 Running manual AI service tests...")
    print("=" * 60)
    
    try:
        # Test initialization
        print("1. Testing AI service initialization...")
        ai_service = GeminiAIService()
        print("   ✅ Service initialized successfully")
        
        # Test connection
        print("\n2. Testing AI connection...")
        success, response = ai_service.test_connection()
        
        if success:
            print("   ✅ Connection successful!")
            print(f"   📝 AI Response: {response[:100]}...")
        else:
            print("   ❌ Connection failed!")
            print(f"   📝 Error: {response}")
            return
        
        # Test exercise plan generation
        print("\n3. Testing exercise plan generation...")
        exercise_result = ai_service.generate_exercise_plan(
            user_goal="build muscle",
            experience_level="intermediate", 
            days_per_week=4,
            user_profile={"age": 25, "gender": "male"}
        )
        
        if exercise_result['success']:
            print("   ✅ Exercise plan generated successfully!")
            plan_data = exercise_result['data']
            print(f"   📝 Plan: {plan_data['plan_name']}")
            print(f"   📝 Description: {plan_data['plan_description']}")
            print(f"   📝 Number of days: {len(plan_data['days'])}")
            
            print("\n   🔍 FULL EXERCISE PLAN OUTPUT:")
            print("   " + "="*80)
            print(json.dumps(plan_data, indent=4))
            print("   " + "="*80)
        else:
            print("   ❌ Exercise plan generation failed!")
            print(f"   📝 Error: {exercise_result.get('error', 'Unknown error')}")
            if 'raw_response' in exercise_result:
                print(f"   📝 Raw AI Response: {exercise_result['raw_response']}")
        
        # Test meal plan generation
        print("\n4. Testing meal plan generation...")
        meal_result = ai_service.generate_meal_plan(
            user_goal="lose weight",
            daily_calorie_target=1800,
            dietary_preferences=["vegetarian"],
            user_profile={"age": 30, "gender": "female"}
        )
        
        if meal_result['success']:
            print("   ✅ Meal plan generated successfully!")
            plan_data = meal_result['data']
            print(f"   📝 Plan: {plan_data['plan_name']}")
            print(f"   📝 Description: {plan_data['plan_description']}")
            print(f"   📝 Number of days: {len(plan_data['days'])}")
            
            # Show nutrition data for first day
            if plan_data['days'] and 'daily_totals' in plan_data['days'][0]:
                daily_totals = plan_data['days'][0]['daily_totals']
                print(f"   📝 Day 1 Nutrition: {daily_totals['calories']} cal, {daily_totals['protein']}g protein")
            
            print("\n   🔍 FULL MEAL PLAN OUTPUT:")
            print("   " + "="*80)
            print(json.dumps(plan_data, indent=4))
            print("   " + "="*80)
        else:
            print("   ❌ Meal plan generation failed!")
            print(f"   📝 Error: {meal_result.get('error', 'Unknown error')}")
            if 'raw_response' in meal_result:
                print(f"   📝 Raw AI Response: {meal_result['raw_response']}")
            
    except Exception as e:
        print(f"   ❌ Test failed with error: {e}")
    
    print("\n" + "=" * 60)
    print("🏁 Manual test completed")


if __name__ == "__main__":
    # Run manual test when executed directly
    run_manual_test()