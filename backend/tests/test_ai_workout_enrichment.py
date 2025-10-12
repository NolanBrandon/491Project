#!/usr/bin/env python3
"""
Comprehensive test: AI Workout Plan Generation + ExerciseDB Enrichment
This test generates a real AI workout plan and enriches it with ExerciseDB data.
"""

import sys
import os
import json
import datetime
from pathlib import Path

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.services.ai_service import GeminiAIService
from api.services.exercise_service import ExerciseDBService


def create_test_user_profiles():
    """Create diverse test user profiles for workout generation."""
    return [
        {
            "name": "Beginner Sarah",
            "user_goal": "lose weight",
            "experience_level": "beginner",
            "days_per_week": 3,
            "user_profile": {
                "age": 28,
                "gender": "female",
                "weight_kg": 70,
                "height_cm": 165,
                "activity_level": "sedentary"
            }
        },
        {
            "name": "Intermediate Mike",
            "user_goal": "build muscle",
            "experience_level": "intermediate", 
            "days_per_week": 4,
            "user_profile": {
                "age": 32,
                "gender": "male",
                "weight_kg": 80,
                "height_cm": 178,
                "activity_level": "moderately_active"
            }
        },
        {
            "name": "Advanced Alex",
            "user_goal": "improve strength",
            "experience_level": "advanced",
            "days_per_week": 5,
            "user_profile": {
                "age": 26,
                "gender": "non-binary",
                "weight_kg": 75,
                "height_cm": 172,
                "activity_level": "very_active"
            }
        }
    ]


def format_enriched_plan_for_file(enriched_plan, user_info):
    """Format the enriched workout plan for readable file output."""
    output = []
    output.append("=" * 80)
    output.append(f"ENRICHED WORKOUT PLAN FOR: {user_info['name']}")
    output.append("=" * 80)
    output.append(f"Goal: {user_info['user_goal']}")
    output.append(f"Experience Level: {user_info['experience_level']}")
    output.append(f"Days per Week: {user_info['days_per_week']}")
    output.append(f"User Profile: {user_info['user_profile']}")
    output.append("")
    
    if enriched_plan.get('success'):
        data = enriched_plan['data']
        
        # Plan overview
        output.append(f"PLAN NAME: {data.get('plan_name', 'N/A')}")
        output.append(f"DESCRIPTION: {data.get('plan_description', 'N/A')}")
        output.append("")
        
        # Enrichment statistics
        stats = enriched_plan.get('enrichment_stats', {})
        output.append("ENRICHMENT STATISTICS:")
        output.append("-" * 40)
        output.append(f"Total Exercises: {stats.get('total_exercises', 0)}")
        output.append(f"Successfully Enriched: {stats.get('total_enriched', 0)}")
        output.append(f"Enrichment Rate: {stats.get('enrichment_rate', 0)}%")
        output.append(f"High Confidence Matches: {stats.get('high_confidence_matches', 0)}")
        output.append(f"Medium Confidence Matches: {stats.get('medium_confidence_matches', 0)}")
        output.append(f"No Matches: {stats.get('no_matches', 0)}")
        output.append("")
        
        # Days and exercises
        for day in data.get('days', []):
            output.append(f"DAY {day.get('day_number', 'N/A')}: {day.get('day_name', 'N/A')}")
            output.append("=" * 60)
            
            if day.get('day_description'):
                output.append(f"Description: {day['day_description']}")
                output.append("")
            
            for i, exercise in enumerate(day.get('exercises', []), 1):
                output.append(f"{i}. {exercise.get('exercise_name', 'N/A')}")
                output.append(f"   Sets: {exercise.get('sets', 'N/A')} | Reps: {exercise.get('reps', 'N/A')}")
                
                # Enrichment info
                data_source = exercise.get('data_source', 'unknown')
                confidence = exercise.get('match_confidence', 'unknown')
                strategy = exercise.get('search_strategy', 'unknown')
                
                output.append(f"   Data Source: {data_source} | Confidence: {confidence} | Strategy: {strategy}")
                
                if exercise.get('matched_exercise_name'):
                    output.append(f"   Matched to: {exercise['matched_exercise_name']}")
                
                # Exercise details from ExerciseDB
                details = exercise.get('exercise_details')
                if details:
                    output.append(f"   Exercise ID: {details.get('exerciseId', 'N/A')}")
                    output.append(f"   Body Parts: {', '.join(details.get('bodyParts', []))}")
                    output.append(f"   Equipment: {', '.join(details.get('equipments', []))}")
                    output.append(f"   Exercise Type: {details.get('exerciseType', 'N/A')}")
                    
                    if details.get('overview'):
                        overview = details['overview']
                        if len(overview) > 200:
                            overview = overview[:200] + "..."
                        output.append(f"   Overview: {overview}")
                    
                    if details.get('instructions'):
                        output.append(f"   Instructions ({len(details['instructions'])} steps):")
                        for j, instruction in enumerate(details['instructions'][:3], 1):  # Show first 3
                            output.append(f"     {j}. {instruction}")
                        if len(details['instructions']) > 3:
                            output.append(f"     ... and {len(details['instructions']) - 3} more steps")
                    
                    if details.get('exerciseTips'):
                        output.append(f"   Tips ({len(details['exerciseTips'])} available):")
                        for j, tip in enumerate(details['exerciseTips'][:2], 1):  # Show first 2
                            tip_preview = tip[:100] + "..." if len(tip) > 100 else tip
                            output.append(f"     • {tip_preview}")
                        if len(details['exerciseTips']) > 2:
                            output.append(f"     ... and {len(details['exerciseTips']) - 2} more tips")
                    
                    if details.get('variations'):
                        output.append(f"   Variations ({len(details['variations'])} available):")
                        for j, variation in enumerate(details['variations'][:2], 1):  # Show first 2
                            var_preview = variation[:100] + "..." if len(variation) > 100 else variation
                            output.append(f"     • {var_preview}")
                        if len(details['variations']) > 2:
                            output.append(f"     ... and {len(details['variations']) - 2} more variations")
                    
                    if details.get('imageUrl'):
                        output.append(f"   Image: {details['imageUrl']}")
                    
                    if details.get('videoUrl'):
                        output.append(f"   Video: {details['videoUrl']}")
                    
                    if details.get('relatedExerciseIds'):
                        output.append(f"   Related Exercises: {len(details['relatedExerciseIds'])} available")
                
                output.append("")  # Empty line between exercises
            
            output.append("")  # Empty line between days
    else:
        output.append(f"❌ ENRICHMENT FAILED: {enriched_plan.get('message', 'Unknown error')}")
    
    return "\n".join(output)


def test_ai_workout_generation_and_enrichment():
    """Test complete workflow: AI generation → ExerciseDB enrichment → File output."""
    print("=" * 80)
    print("AI WORKOUT PLAN GENERATION + EXERCISEDB ENRICHMENT TEST")
    print("=" * 80)
    
    # Initialize services
    try:
        print("Initializing AI service...")
        ai_service = GeminiAIService()
        print("✅ AI service initialized")
        
        print("Initializing ExerciseDB service...")
        exercise_service = ExerciseDBService()
        print("✅ ExerciseDB service initialized")
    except Exception as e:
        print(f"❌ Failed to initialize services: {e}")
        return
    
    # Test AI connection
    print("\nTesting AI connection...")
    ai_success, ai_message = ai_service.test_connection()
    if ai_success:
        print(f"✅ AI connection successful")
    else:
        print(f"❌ AI connection failed: {ai_message}")
        return
    
    # Test ExerciseDB connection
    print("Testing ExerciseDB connection...")
    db_success, db_message = exercise_service.test_connection()
    if db_success:
        print(f"✅ ExerciseDB connection successful")
    else:
        print(f"❌ ExerciseDB connection failed: {db_message}")
        return
    
    # Create output directory
    output_dir = Path("/Users/ivanflores/capstone/backend/test_output")
    output_dir.mkdir(exist_ok=True)
    
    # Test with different user profiles
    test_profiles = create_test_user_profiles()
    
    for i, profile in enumerate(test_profiles, 1):
        print(f"\n{'-' * 60}")
        print(f"TEST {i}: {profile['name']}")
        print(f"{'-' * 60}")
        
        try:
            # Generate AI workout plan
            print(f"📝 Generating AI workout plan for {profile['name']}...")
            ai_plan = ai_service.generate_exercise_plan(
                user_goal=profile['user_goal'],
                experience_level=profile['experience_level'],
                days_per_week=profile['days_per_week'],
                user_profile=profile['user_profile']
            )
            
            if ai_plan.get('success'):
                print(f"✅ AI workout plan generated successfully")
                print(f"   Plan: {ai_plan['data'].get('plan_name', 'N/A')}")
                print(f"   Days: {len(ai_plan['data'].get('days', []))}")
                
                total_exercises = sum(len(day.get('exercises', [])) for day in ai_plan['data'].get('days', []))
                print(f"   Total exercises: {total_exercises}")
                
                # Enrich with ExerciseDB
                print(f"🔄 Enriching workout plan with ExerciseDB data...")
                enriched_plan = exercise_service.enrich_workout_plan(ai_plan)
                
                if enriched_plan.get('success'):
                    stats = enriched_plan.get('enrichment_stats', {})
                    print(f"✅ Enrichment successful!")
                    print(f"   Enrichment rate: {stats.get('enrichment_rate', 0)}%")
                    print(f"   High confidence matches: {stats.get('high_confidence_matches', 0)}")
                    print(f"   Total enriched: {stats.get('total_enriched', 0)}/{stats.get('total_exercises', 0)}")
                    
                    # Write to file
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"enriched_workout_plan_{profile['name'].lower().replace(' ', '_')}_{timestamp}.txt"
                    filepath = output_dir / filename
                    
                    formatted_output = format_enriched_plan_for_file(enriched_plan, profile)
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(formatted_output)
                    
                    print(f"📄 Enriched plan written to: {filepath}")
                    
                    # Also write JSON for detailed analysis
                    json_filename = f"enriched_workout_plan_{profile['name'].lower().replace(' ', '_')}_{timestamp}.json"
                    json_filepath = output_dir / json_filename
                    
                    with open(json_filepath, 'w', encoding='utf-8') as f:
                        json.dump(enriched_plan, f, indent=2, default=str)
                    
                    print(f"📄 JSON data written to: {json_filepath}")
                    
                else:
                    print(f"❌ Enrichment failed: {enriched_plan.get('message', 'Unknown error')}")
                    
            else:
                print(f"❌ AI workout plan generation failed: {ai_plan.get('message', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ Error in test {i}: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'=' * 80}")
    print("TEST COMPLETED")
    print(f"Output files saved to: {output_dir}")
    print(f"{'=' * 80}")


if __name__ == "__main__":
    test_ai_workout_generation_and_enrichment()