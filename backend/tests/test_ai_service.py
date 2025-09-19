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
    
    def test_exercise_plan_generation(self):
        """Test that the exercise plan generation works with new structure."""
        try:
            self.ai_service = GeminiAIService()
            
            # Test data for exercise plan
            user_goal = "build muscle"
            experience_level = "intermediate"
            days_per_week = 4
            user_profile = {"age": 25, "gender": "male"}
            
            result = self.ai_service.generate_exercise_plan(
                user_goal, experience_level, days_per_week, user_profile
            )
            
            self.assertIsInstance(result, dict)
            self.assertIn('success', result)
            self.assertIn('data', result)
            self.assertIn('message', result)
            
            if result['success']:
                plan_data = result['data']
                self.assertIn('plan_name', plan_data)
                self.assertIn('plan_description', plan_data)
                self.assertIn('days', plan_data)
                self.assertIsInstance(plan_data['days'], list)
                
                # Check first day structure
                if plan_data['days']:
                    first_day = plan_data['days'][0]
                    self.assertIn('day_number', first_day)
                    self.assertIn('exercises', first_day)
                    
                print(f"✅ Exercise plan generation test passed")
                print(f"   Plan: {plan_data['plan_name']}")
                print(f"   Days: {len(plan_data['days'])}")
            else:
                print(f"⚠️  Exercise plan generation returned error: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            self.fail(f"Exercise plan generation test failed: {e}")
    
    def test_meal_plan_generation(self):
        """Test that the meal plan generation works with new structure and nutrition data."""
        try:
            self.ai_service = GeminiAIService()
            
            # Test data for meal plan
            user_goal = "lose weight"
            daily_calorie_target = 1800
            dietary_preferences = ["vegetarian"]
            user_profile = {"age": 30, "gender": "female"}
            
            result = self.ai_service.generate_meal_plan(
                user_goal, daily_calorie_target, dietary_preferences, user_profile
            )
            
            self.assertIsInstance(result, dict)
            self.assertIn('success', result)
            self.assertIn('data', result)
            self.assertIn('message', result)
            
            if result['success']:
                plan_data = result['data']
                self.assertIn('plan_name', plan_data)
                self.assertIn('plan_description', plan_data)
                self.assertIn('days', plan_data)
                self.assertIsInstance(plan_data['days'], list)
                
                # Check first day structure and nutrition data
                if plan_data['days']:
                    first_day = plan_data['days'][0]
                    self.assertIn('day_number', first_day)
                    self.assertIn('meals', first_day)
                    
                    meals = first_day['meals']
                    if 'breakfast' in meals:
                        breakfast = meals['breakfast']
                        self.assertIn('recipe_name', breakfast)
                        self.assertIn('ingredients', breakfast)
                        self.assertIn('meal_totals', breakfast)
                        
                        # Check nutrition data structure
                        meal_totals = breakfast['meal_totals']
                        nutrition_fields = ['calories', 'protein', 'carbs', 'fat', 'trans_fat', 'fiber', 'sugar']
                        for field in nutrition_fields:
                            self.assertIn(field, meal_totals)
                        
                        # Check ingredient nutrition
                        if breakfast['ingredients']:
                            ingredient = breakfast['ingredients'][0]
                            for field in nutrition_fields:
                                self.assertIn(field, ingredient)
                    
                    # Check daily totals
                    if 'daily_totals' in first_day:
                        daily_totals = first_day['daily_totals']
                        nutrition_fields = ['calories', 'protein', 'carbs', 'fat', 'trans_fat', 'fiber', 'sugar']
                        for field in nutrition_fields:
                            self.assertIn(field, daily_totals)
                
                print(f"✅ Meal plan generation test passed")
                print(f"   Plan: {plan_data['plan_name']}")
                print(f"   Days: {len(plan_data['days'])}")
                if plan_data['days'] and 'daily_totals' in plan_data['days'][0]:
                    daily_cals = plan_data['days'][0]['daily_totals']['calories']
                    print(f"   Day 1 Calories: {daily_cals}")
            else:
                print(f"⚠️  Meal plan generation returned error: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            self.fail(f"Meal plan generation test failed: {e}")
    
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