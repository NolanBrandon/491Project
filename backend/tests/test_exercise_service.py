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
    
    # Test 7: Get Equipment Types
    print("\n7. Testing Get Equipment Types")
    print("-" * 40)
    equipment_result = service.get_equipments()
    if equipment_result['success']:
        equipment_count = len(equipment_result['data'].get('data', []))
        print(f"✅ Get equipment types successful: Found {equipment_count} equipment types")
        # Show first few equipment types
        equipments = equipment_result['data'].get('data', [])
        for i, equipment in enumerate(equipments[:5]):
            if isinstance(equipment, dict):
                print(f"   {i+1}. {equipment.get('name', equipment)}")
            else:
                print(f"   {i+1}. {equipment}")
    else:
        print(f"❌ Get equipment types failed: {equipment_result['message']}")
    
    # Test 8: Get Exercise Types
    print("\n8. Testing Get Exercise Types")
    print("-" * 40)
    exercise_types_result = service.get_exercise_types()
    if exercise_types_result['success']:
        types_count = len(exercise_types_result['data'].get('data', []))
        print(f"✅ Get exercise types successful: Found {types_count} exercise types")
        # Show first few exercise types
        exercise_types = exercise_types_result['data'].get('data', [])
        for i, ex_type in enumerate(exercise_types[:5]):
            if isinstance(ex_type, dict):
                print(f"   {i+1}. {ex_type.get('name', ex_type)}")
            else:
                print(f"   {i+1}. {ex_type}")
    else:
        print(f"❌ Get exercise types failed: {exercise_types_result['message']}")
    
    # Test 9: Get Body Parts
    print("\n9. Testing Get Body Parts")
    print("-" * 40)
    bodyparts_result = service.get_bodyparts()
    if bodyparts_result['success']:
        bodyparts_count = len(bodyparts_result['data'].get('data', []))
        print(f"✅ Get body parts successful: Found {bodyparts_count} body parts")
        # Show first few body parts
        bodyparts = bodyparts_result['data'].get('data', [])
        for i, bodypart in enumerate(bodyparts[:5]):
            if isinstance(bodypart, dict):
                print(f"   {i+1}. {bodypart.get('name', bodypart)}")
            else:
                print(f"   {i+1}. {bodypart}")
    else:
        print(f"❌ Get body parts failed: {bodyparts_result['message']}")
    
    # Test 10: Get Muscles
    print("\n10. Testing Get Muscles")
    print("-" * 40)
    muscles_result = service.get_muscles()
    if muscles_result['success']:
        muscles_count = len(muscles_result['data'].get('data', []))
        print(f"✅ Get muscles successful: Found {muscles_count} muscle groups")
        # Show first few muscle groups
        muscles = muscles_result['data'].get('data', [])
        for i, muscle in enumerate(muscles[:5]):
            if isinstance(muscle, dict):
                print(f"   {i+1}. {muscle.get('name', muscle)}")
            else:
                print(f"   {i+1}. {muscle}")
    else:
        print(f"❌ Get muscles failed: {muscles_result['message']}")
    
    # Test 11: Get All Reference Data
    print("\n11. Testing Get All Reference Data")
    print("-" * 40)
    reference_data_result = service.get_reference_data()
    if reference_data_result['success']:
        counts = reference_data_result.get('counts', {})
        print("✅ Get all reference data successful")
        print(f"   Equipment types: {counts.get('equipments', 0)}")
        print(f"   Exercise types: {counts.get('exercise_types', 0)}")
        print(f"   Body parts: {counts.get('bodyparts', 0)}")
        print(f"   Muscle groups: {counts.get('muscles', 0)}")
    else:
        print(f"❌ Get all reference data failed: {reference_data_result['message']}")
    
    # Test 12: Get Exercises by Filters
    print("\n12. Testing Get Exercises by Filters")
    print("-" * 40)
    
    # Test filtering by equipment
    barbell_exercises = service.get_exercises_by_filters(equipment="barbell", limit=5)
    if barbell_exercises['success']:
        count = len(barbell_exercises['data'].get('data', []))
        print(f"✅ Barbell exercises filter successful: Found {count} exercises")
    else:
        print(f"❌ Barbell exercises filter failed: {barbell_exercises['message']}")
    
    # Test filtering by body part
    chest_exercises = service.get_exercises_by_filters(bodypart="chest", limit=5)
    if chest_exercises['success']:
        count = len(chest_exercises['data'].get('data', []))
        print(f"✅ Chest exercises filter successful: Found {count} exercises")
    else:
        print(f"❌ Chest exercises filter failed: {chest_exercises['message']}")
    
    # Test filtering by exercise type
    strength_exercises = service.get_exercises_by_filters(exercise_type="strength", limit=5)
    if strength_exercises['success']:
        count = len(strength_exercises['data'].get('data', []))
        print(f"✅ Strength exercises filter successful: Found {count} exercises")
    else:
        print(f"❌ Strength exercises filter failed: {strength_exercises['message']}")
    
    print("\n" + "=" * 60)
    print("TESTING COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    test_exercise_service()