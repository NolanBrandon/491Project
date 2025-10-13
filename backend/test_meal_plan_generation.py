#!/usr/bin/env python
"""
Test script for AI meal plan generation.
This script tests the meal plan generation functionality independently.
"""

import os
import sys
import django
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'easyfitness_backend.settings')
django.setup()

from api.services.ai_service import GeminiAIService
import json
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_meal_plan_generation():
    """Test meal plan generation with various parameters."""
    
    print("🍽️ Starting Meal Plan Generation Test")
    print("=" * 50)
    
    try:
        # Initialize AI service
        print("🤖 Initializing Gemini AI service...")
        ai_service = GeminiAIService()
        
        # Test connection first
        print("🔗 Testing AI connection...")
        success, message = ai_service.test_connection()
        if not success:
            print(f"❌ AI connection failed: {message}")
            return
        print(f"✅ AI connection successful: {message[:100]}...")
        
        # Test simple meal plan generation
        print("\n📋 Testing Simple Meal Plan Generation...")
        test_cases = [
            {
                "name": "Simple 3-Day Plan",
                "user_goal": "maintain weight",
                "daily_calorie_target": 2000,
                "dietary_preferences": ["balanced"],
                "user_profile": {"age": 25, "gender": "female", "activity_level": "moderate"}
            },
            {
                "name": "High Protein Plan",
                "user_goal": "build muscle",
                "daily_calorie_target": 2500,
                "dietary_preferences": ["high protein"],
                "user_profile": {"age": 28, "gender": "male", "activity_level": "very active"}
            },
            {
                "name": "Weight Loss Plan",
                "user_goal": "lose weight",
                "daily_calorie_target": 1800,
                "dietary_preferences": ["low carb"],
                "user_profile": {"age": 30, "gender": "female", "activity_level": "active"}
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n🧪 Test Case {i}: {test_case['name']}")
            print(f"   Goal: {test_case['user_goal']}")
            print(f"   Calories: {test_case['daily_calorie_target']}")
            print(f"   Preferences: {test_case['dietary_preferences']}")
            
            try:
                # Generate meal plan
                print("   ⏱️ Generating meal plan (this may take 30-60 seconds)...")
                result = ai_service.generate_meal_plan(
                    user_goal=test_case['user_goal'],
                    daily_calorie_target=test_case['daily_calorie_target'],
                    dietary_preferences=test_case['dietary_preferences'],
                    user_profile=test_case['user_profile']
                )
                
                if result.get('success'):
                    meal_plan = result['data']
                    print(f"   ✅ Success! Generated: {meal_plan.get('plan_name', 'Unknown Plan')}")
                    print(f"   📅 Days: {len(meal_plan.get('days', []))}")
                    
                    # Show first day meals
                    if meal_plan.get('days'):
                        first_day = meal_plan['days'][0]
                        meals = first_day.get('meals', {})
                        print(f"   🍽️ Day 1 meals: {list(meals.keys())}")
                        
                        # Show breakfast details
                        if 'breakfast' in meals:
                            breakfast = meals['breakfast']
                            print(f"   🥞 Breakfast: {breakfast.get('recipe_name', 'Unknown Recipe')}")
                            ingredients = breakfast.get('ingredients', [])
                            print(f"   🥗 Ingredients: {len(ingredients)} items")
                    
                    # Save result to file for inspection
                    filename = f"test_meal_plan_{i}_{test_case['name'].lower().replace(' ', '_')}.json"
                    with open(filename, 'w') as f:
                        json.dump(meal_plan, f, indent=2)
                    print(f"   💾 Saved to: {filename}")
                    
                else:
                    print(f"   ❌ Failed: {result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                print(f"   ❌ Exception: {str(e)}")
                logger.error(f"Test case {i} failed", exc_info=True)
            
            print("   " + "-" * 40)
    
    except Exception as e:
        print(f"❌ Test setup failed: {str(e)}")
        logger.error("Test setup failed", exc_info=True)
    
    print("\n🏁 Meal Plan Generation Test Complete")

def test_minimal_meal_plan():
    """Test with minimal parameters to isolate issues."""
    
    print("\n🔬 Testing Minimal Meal Plan Generation")
    print("=" * 50)
    
    try:
        ai_service = GeminiAIService()
        
        # Very simple request
        print("📝 Generating minimal meal plan...")
        result = ai_service.generate_meal_plan(
            user_goal="maintain weight",
            daily_calorie_target=2000,
            dietary_preferences=[],  # No specific preferences
            user_profile={"age": 25, "gender": "female"}
        )
        
        if result.get('success'):
            print("✅ Minimal test successful!")
            meal_plan = result['data']
            print(f"Plan: {meal_plan.get('plan_name', 'No name')}")
            print(f"Days: {len(meal_plan.get('days', []))}")
        else:
            print(f"❌ Minimal test failed: {result.get('error')}")
            
    except Exception as e:
        print(f"❌ Minimal test exception: {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting Meal Plan AI Test Suite")
    print(f"📁 Working directory: {os.getcwd()}")
    print(f"🐍 Python path: {sys.path[0]}")
    
    # Run tests
    test_meal_plan_generation()
    test_minimal_meal_plan()
    
    print("\n🎯 All tests completed!")
    print("Check generated JSON files for detailed meal plan data.")