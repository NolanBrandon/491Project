"""
Debug script to examine ExerciseDB API response structure
"""

import sys
import os
import json

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.services.exercise_service import ExerciseDBService


def debug_api_responses():
    """Debug the actual API response structures."""
    print("=" * 60)
    print("DEBUGGING EXERCISEDB API RESPONSES")
    print("=" * 60)
    
    service = ExerciseDBService()
    
    # Test search endpoint
    print("\n1. SEARCH EXERCISES RESPONSE:")
    print("-" * 40)
    search_result = service.search_exercises("push up")
    if search_result['success']:
        data = search_result['data']
        print(f"Raw response keys: {list(data.keys())}")
        
        exercises = data.get('data', [])
        if exercises:
            first_exercise = exercises[0]
            print(f"First exercise type: {type(first_exercise)}")
            if isinstance(first_exercise, dict):
                print(f"First exercise keys: {list(first_exercise.keys())}")
                print(f"First exercise sample: {json.dumps(first_exercise, indent=2)}")
            else:
                print(f"First exercise value: {first_exercise}")
    
    # Test get exercises endpoint  
    print("\n2. GET EXERCISES RESPONSE:")
    print("-" * 40)
    get_result = service.get_exercises(name="push up", limit=3)
    if get_result['success']:
        data = get_result['data']
        print(f"Raw response keys: {list(data.keys())}")
        
        exercises = data.get('data', [])
        if exercises:
            first_exercise = exercises[0]
            print(f"First exercise type: {type(first_exercise)}")
            if isinstance(first_exercise, dict):
                print(f"First exercise keys: {list(first_exercise.keys())}")
                print(f"First exercise sample: {json.dumps(first_exercise, indent=2)}")
            else:
                print(f"First exercise value: {first_exercise}")


if __name__ == "__main__":
    debug_api_responses()