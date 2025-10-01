"""
Test script for ExerciseDB API service endpoints.
This script tests all the implemented endpoints to ensure they work correctly.
"""

import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.services.exercise_service import ExerciseDBService
import json


def test_exercise_service():
    """Test all ExerciseDB service endpoints."""
    print("=" * 60)
    print("TESTING EXERCISEDB API SERVICE")
    print("=" * 60)
    
    # Initialize the service
    try:
        service = ExerciseDBService()
        print("✅ Service initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize service: {e}")
        return
    
    # Test 1: Connection test
    print("\n1. Testing API Connection (Liveness Endpoint)")
    print("-" * 40)
    success, message = service.test_connection()
    if success:
        print(f"✅ Connection test passed: {message}")
    else:
        print(f"❌ Connection test failed: {message}")
    
    # Test 2: Get exercises with parameters
    print("\n2. Testing Get Exercises with Parameters")
    print("-" * 40)
    result = service.get_exercises(name="Bench Press", keywords="chest workout,barbell", limit=5)
    if result['success']:
        print(f"✅ Get exercises successful: Found {len(result['data'].get('data', []))} exercises")
        # Print first exercise if available
        exercises = result['data'].get('data', [])
        if exercises:
            first_exercise = exercises[0]
            print(f"   First exercise: {first_exercise.get('name', 'N/A')}")
            print(f"   Target: {first_exercise.get('target', 'N/A')}")
            print(f"   Equipment: {first_exercise.get('equipment', 'N/A')}")
    else:
        print(f"❌ Get exercises failed: {result['message']}")
    
    # Test 3: Search exercises
    print("\n3. Testing Exercise Search")
    print("-" * 40)
    search_result = service.search_exercises("strength exercises")
    if search_result['success']:
        print(f"✅ Exercise search successful: Found {len(search_result['data'].get('data', []))} results")
        # Print first few results
        exercises = search_result['data'].get('data', [])
        for i, exercise in enumerate(exercises[:3]):
            print(f"   {i+1}. {exercise.get('name', 'N/A')} - {exercise.get('bodyPart', 'N/A')}")
    else:
        print(f"❌ Exercise search failed: {search_result['message']}")
    
    # Test 4: Get exercise by ID (using a known ID from previous tests)
    print("\n4. Testing Get Exercise by ID")
    print("-" * 40)
    # Try to get an ID from previous results
    exercise_id = None
    if 'exercises' in locals() and exercises:
        exercise_id = exercises[0].get('id')
    
    if exercise_id:
        id_result = service.get_exercise_by_id(exercise_id)
        if id_result['success']:
            print(f"✅ Get exercise by ID successful")
            exercise_data = id_result['data']
            if 'data' in exercise_data:
                exercise = exercise_data['data']
                print(f"   Exercise: {exercise.get('name', 'N/A')}")
                print(f"   ID: {exercise.get('id', 'N/A')}")
                print(f"   Instructions: {len(exercise.get('instructions', []))} steps")
        else:
            print(f"❌ Get exercise by ID failed: {id_result['message']}")
    else:
        print("⚠️  Skipping ID test - no exercise ID available from previous tests")
    
    # Test 5: Test workout plan enrichment
    print("\n5. Testing Workout Plan Enrichment")
    print("-" * 40)
    
    # Create a mock workout plan similar to what AI service would return
    mock_workout_plan = {
        "success": True,
        "data": {
            "plan_name": "Test Workout Plan",
            "plan_description": "A test plan for API integration",
            "days": [
                {
                    "day_number": 1,
                    "day_name": "Upper Body",
                    "exercises": [
                        {
                            "exercise_name": "Push-up",
                            "sets": 3,
                            "reps": "10-15"
                        },
                        {
                            "exercise_name": "Pull-up",
                            "sets": 3,
                            "reps": "5-10"
                        }
                    ]
                }
            ]
        },
        "message": "Workout plan generated successfully"
    }
    
    enriched_result = service.enrich_workout_plan(mock_workout_plan)
    if enriched_result['success']:
        print("✅ Workout plan enrichment successful")
        stats = enriched_result.get('enrichment_stats', {})
        print(f"   Total exercises: {stats.get('total_exercises', 0)}")
        print(f"   Enriched exercises: {stats.get('enriched_exercises', 0)}")
        print(f"   Enrichment rate: {stats.get('enrichment_rate', 0)}%")
        
        # Show details of enriched exercises
        enriched_days = enriched_result['data']['days']
        for day in enriched_days:
            print(f"\n   Day: {day['day_name']}")
            for exercise in day['exercises']:
                print(f"     - {exercise['exercise_name']}: {exercise['data_source']}")
                if exercise.get('exercise_details'):
                    details = exercise['exercise_details']
                    print(f"       Target: {details.get('target', 'N/A')}")
                    print(f"       Equipment: {details.get('equipment', 'N/A')}")
    else:
        print(f"❌ Workout plan enrichment failed: {enriched_result['message']}")
    
    # Test 6: Get exercise suggestions
    print("\n6. Testing Exercise Suggestions")
    print("-" * 40)
    exercise_names = ["Squats", "Deadlift", "Bench Press"]
    suggestions_result = service.get_exercise_suggestions(exercise_names)
    if suggestions_result['success']:
        print("✅ Exercise suggestions successful")
        suggestions_data = suggestions_result['data']
        for exercise_name, result in suggestions_data.items():
            if result['success']:
                count = len(result['data'].get('data', []))
                print(f"   {exercise_name}: Found {count} matches")
            else:
                print(f"   {exercise_name}: No matches found")
    else:
        print(f"❌ Exercise suggestions failed: {suggestions_result['message']}")
    
    print("\n" + "=" * 60)
    print("TESTING COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    test_exercise_service()