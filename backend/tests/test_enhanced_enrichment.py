#!/usr/bin/env python3
"""
Test the enhanced enrichment with more challenging exercise names
"""

import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.services.exercise_service import ExerciseDBService


def test_enhanced_enrichment():
    """Test enrichment with challenging exercise names."""
    print("=" * 60)
    print("TESTING ENHANCED WORKOUT PLAN ENRICHMENT")
    print("=" * 60)
    
    # Initialize the service
    try:
        service = ExerciseDBService()
        print("✅ Service initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize service: {e}")
        return
    
    # Create a challenging workout plan with varied exercise names
    challenging_workout_plan = {
        "success": True,
        "data": {
            "plan_name": "Challenging Exercise Matching Test",
            "plan_description": "Tests various exercise name formats for matching",
            "days": [
                {
                    "day_number": 1,
                    "day_name": "Mixed Exercises",
                    "exercises": [
                        # Standard names
                        {
                            "exercise_name": "Push-up",
                            "sets": 3,
                            "reps": "10-15"
                        },
                        # Alternative spellings
                        {
                            "exercise_name": "Pushup",
                            "sets": 3,
                            "reps": "10-15"
                        },
                        # With spaces vs hyphens
                        {
                            "exercise_name": "Pull up",
                            "sets": 3,
                            "reps": "5-10"
                        },
                        # Abbreviations
                        {
                            "exercise_name": "DB Press",
                            "sets": 3,
                            "reps": "8-12"
                        },
                        # Common variations
                        {
                            "exercise_name": "Bench Press",
                            "sets": 3,
                            "reps": "8-10"
                        },
                        # Partial names
                        {
                            "exercise_name": "Squat",
                            "sets": 3,
                            "reps": "10-15"
                        },
                        # Made-up exercise (should fail to match)
                        {
                            "exercise_name": "Magic Flying Exercise",
                            "sets": 3,
                            "reps": "1-100"
                        }
                    ]
                }
            ]
        },
        "message": "Challenging workout plan generated for testing"
    }
    
    # Test enrichment
    print("\nTesting Enhanced Enrichment...")
    print("-" * 40)
    
    enriched_result = service.enrich_workout_plan(challenging_workout_plan)
    
    if enriched_result['success']:
        print("✅ Enhanced workout plan enrichment successful!")
        
        stats = enriched_result.get('enrichment_stats', {})
        print(f"\nEnrichment Statistics:")
        print(f"   Total exercises: {stats.get('total_exercises', 0)}")
        print(f"   Detailed enriched: {stats.get('detailed_enriched', 0)}")
        print(f"   Search enriched: {stats.get('search_enriched', 0)}")
        print(f"   AI only: {stats.get('ai_only', 0)}")
        print(f"   Overall enrichment rate: {stats.get('enrichment_rate', 0)}%")
        print(f"   High confidence matches: {stats.get('high_confidence_matches', 0)}")
        print(f"   Medium confidence matches: {stats.get('medium_confidence_matches', 0)}")
        print(f"   No matches: {stats.get('no_matches', 0)}")
        print(f"   High confidence rate: {stats.get('high_confidence_rate', 0)}%")
        
        # Show detailed results for each exercise
        enriched_days = enriched_result['data']['days']
        for day in enriched_days:
            print(f"\n{day['day_name']}:")
            print("-" * 30)
            
            for i, exercise in enumerate(day['exercises'], 1):
                original_name = exercise['exercise_name']
                data_source = exercise['data_source']
                confidence = exercise.get('match_confidence', 'unknown')
                strategy = exercise.get('search_strategy', 'unknown')
                matched_name = exercise.get('matched_exercise_name', 'N/A')
                
                print(f"{i:2d}. Original: '{original_name}'")
                print(f"    Status: {data_source} (confidence: {confidence})")
                print(f"    Strategy: {strategy}")
                
                if matched_name != 'N/A':
                    print(f"    Matched: '{matched_name}'")
                    
                    if exercise.get('exercise_details'):
                        details = exercise['exercise_details']
                        print(f"    Body Parts: {details.get('bodyParts', 'N/A')}")
                        print(f"    Equipment: {details.get('equipments', 'N/A')}")
                        print(f"    Type: {details.get('exerciseType', 'N/A')}")
                        
                        instructions = details.get('instructions', [])
                        if instructions:
                            print(f"    Instructions: {len(instructions)} steps")
                        
                        tips = details.get('exerciseTips', [])
                        if tips:
                            print(f"    Tips: {len(tips)} available")
                            
                        variations = details.get('variations', [])
                        if variations:
                            print(f"    Variations: {len(variations)} available")
                else:
                    print(f"    Matched: No match found")
                
                print()  # Empty line for readability
    else:
        print(f"❌ Enhanced workout plan enrichment failed: {enriched_result['message']}")
    
    print("=" * 60)
    print("ENHANCED ENRICHMENT TEST COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    test_enhanced_enrichment()