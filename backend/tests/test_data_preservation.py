# #!/usr/bin/env python3
# """
# Test to verify all exercise details are preserved in the enriched workout plan
# """

# import sys
# import os
# import json

# # Add the project root to Python path
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from api.services.exercise_service import ExerciseDBService


# def test_exercise_details_preservation():
#     """Test that all exercise details from get_exercise_by_id are preserved."""
#     print("=" * 60)
#     print("TESTING EXERCISE DETAILS PRESERVATION")
#     print("=" * 60)
    
#     # Initialize the service
#     try:
#         service = ExerciseDBService()
#         print("✅ Service initialized successfully")
#     except Exception as e:
#         print(f"❌ Failed to initialize service: {e}")
#         return
    
#     # Test a single exercise enrichment first to see raw data
#     print("\n1. Testing Raw Exercise Data Retrieval")
#     print("-" * 40)
    
#     # Get a specific exercise by ID to see what data is available
#     search_result = service.search_exercises("Push-up")
#     if search_result.get('success') and search_result['data'].get('data'):
#         exercise_id = search_result['data']['data'][0].get('exerciseId')
#         print(f"Found exercise ID: {exercise_id}")
        
#         detailed_result = service.get_exercise_by_id(exercise_id)
#         if detailed_result.get('success'):
#             raw_data = detailed_result['data'].get('data', detailed_result['data'])
#             print(f"\nRaw Exercise Data from get_exercise_by_id:")
#             print(f"Available fields: {list(raw_data.keys())}")
            
#             # Show actual content for key fields
#             for field in ['exerciseId', 'name', 'overview', 'instructions', 'exerciseTips', 'variations']:
#                 value = raw_data.get(field)
#                 if isinstance(value, list):
#                     print(f"  {field}: {len(value)} items")
#                     if value and len(str(value[0])) < 100:
#                         print(f"    First item: {value[0]}")
#                 elif isinstance(value, str) and len(value) < 200:
#                     print(f"  {field}: {value}")
#                 elif value:
#                     print(f"  {field}: {type(value).__name__} (length: {len(str(value))})")
#                 else:
#                     print(f"  {field}: None/Empty")
    
#     # Test enrichment with a simple workout plan
#     print("\n\n2. Testing Enriched Workout Plan Data")
#     print("-" * 40)
    
#     simple_workout_plan = {
#         "success": True,
#         "data": {
#             "plan_name": "Data Preservation Test",
#             "days": [
#                 {
#                     "day_number": 1,
#                     "day_name": "Test Day",
#                     "exercises": [
#                         {
#                             "exercise_name": "Push-up",
#                             "sets": 3,
#                             "reps": "10-15"
#                         }
#                     ]
#                 }
#             ]
#         }
#     }
    
#     enriched_result = service.enrich_workout_plan(simple_workout_plan)
    
#     if enriched_result['success']:
#         print("✅ Enrichment successful")
        
#         # Extract the enriched exercise
#         enriched_exercise = enriched_result['data']['days'][0]['exercises'][0]
#         exercise_details = enriched_exercise.get('exercise_details', {})
        
#         print(f"\nEnriched Exercise Data:")
#         print(f"Original exercise name: '{enriched_exercise['exercise_name']}'")
#         print(f"Data source: {enriched_exercise.get('data_source')}")
#         print(f"Match confidence: {enriched_exercise.get('match_confidence')}")
#         print(f"Matched name: '{enriched_exercise.get('matched_exercise_name')}'")
        
#         print(f"\nExercise Details Preserved:")
#         for field, value in exercise_details.items():
#             if isinstance(value, list):
#                 print(f"  ✅ {field}: {len(value)} items")
#                 if value:
#                     # Show sample content for arrays
#                     if field in ['instructions', 'exerciseTips', 'variations']:
#                         print(f"      Sample: {value[0][:80]}..." if len(str(value[0])) > 80 else f"      Sample: {value[0]}")
#                     else:
#                         print(f"      Items: {value}")
#             elif isinstance(value, str):
#                 if len(value) > 100:
#                     print(f"  ✅ {field}: {value[:100]}...")
#                 else:
#                     print(f"  ✅ {field}: {value}")
#             elif value is not None:
#                 print(f"  ✅ {field}: {value}")
#             else:
#                 print(f"  ❌ {field}: None/Empty")
        
#         # Check what fields from get_exercise_by_id are preserved
#         print(f"\n3. Field Preservation Analysis")
#         print("-" * 40)
        
#         expected_fields = [
#             'exerciseId', 'name', 'imageUrl', 'videoUrl', 'bodyParts', 
#             'equipments', 'exerciseType', 'targetMuscles', 'secondaryMuscles',
#             'keywords', 'overview', 'instructions', 'exerciseTips', 
#             'variations', 'relatedExerciseIds'
#         ]
        
#         print("Field preservation status:")
#         for field in expected_fields:
#             if field in exercise_details:
#                 value = exercise_details[field]
#                 if value is not None and value != []:
#                     print(f"  ✅ {field}: Preserved and has data")
#                 else:
#                     print(f"  ⚠️  {field}: Preserved but empty")
#             else:
#                 print(f"  ❌ {field}: Missing from enriched data")
        
#         # Show the complete enriched exercise structure
#         print(f"\n4. Complete Enriched Exercise Structure")
#         print("-" * 40)
#         print("Complete enriched exercise (formatted):")
#         print(json.dumps(enriched_exercise, indent=2, default=str)[:2000] + "..." if len(str(enriched_exercise)) > 2000 else json.dumps(enriched_exercise, indent=2, default=str))
        
#     else:
#         print(f"❌ Enrichment failed: {enriched_result['message']}")
    
#     print("\n" + "=" * 60)
#     print("DATA PRESERVATION TEST COMPLETED")
#     print("=" * 60)


# if __name__ == "__main__":
#     test_exercise_details_preservation()