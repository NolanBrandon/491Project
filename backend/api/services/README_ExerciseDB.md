# ExerciseDB API Service Documentation

## Overview
The ExerciseDB Service provides a comprehensive interface to the ExerciseDB API, enabling integration with AI-generated workout plans and exercise data management.

## Features

### Core Endpoints
1. **Connection Testing** - `test_connection()`
   - Tests API connectivity using the liveness endpoint
   - Returns: (success: bool, message: str)

2. **Exercise Retrieval** - `get_exercises(name, keywords, limit)`
   - Retrieves exercises with optional filtering
   - Parameters: name (optional), keywords (optional), limit (default: 10)

3. **Exercise Search** - `search_exercises(search_term)`
   - Search exercises by term
   - Parameter: search_term (required)

4. **Exercise by ID** - `get_exercise_by_id(exercise_id)`
   - Get detailed exercise information by ID
   - Parameter: exercise_id (required)

### Reference Data Endpoints
5. **Equipment Types** - `get_equipments()`
   - Returns all available equipment types (28 types)

6. **Exercise Types** - `get_exercise_types()`
   - Returns all exercise categories (7 types: STRENGTH, CARDIO, etc.)

7. **Body Parts** - `get_bodyparts()`
   - Returns all targetable body parts (18 parts)

8. **Muscle Groups** - `get_muscles()`
   - Returns all muscle groups (3 groups)

### Advanced Features
9. **Workout Plan Enrichment** - `enrich_workout_plan(workout_plan)`
   - Enhances AI-generated workout plans with exercise database details
   - Adds exercise_details, instructions, target muscles, equipment info
   - Returns enrichment statistics

10. **Exercise Suggestions** - `get_exercise_suggestions(exercise_names)`
    - Batch lookup for multiple exercise names
    - Useful for processing AI-generated exercise lists

11. **Combined Reference Data** - `get_reference_data()`
    - Retrieves all reference data in one call
    - Perfect for populating frontend filter options

12. **Filtered Exercise Search** - `get_exercises_by_filters(equipment, bodypart, exercise_type, limit)`
    - Advanced filtering by multiple criteria
    - Combines search with reference data filtering

## Usage Examples

### Basic Exercise Search
```python
service = ExerciseDBService()
result = service.search_exercises("push up")
```

### Enrich AI Workout Plan
```python
# Assuming you have an AI-generated workout plan
enriched_plan = service.enrich_workout_plan(ai_workout_plan)
```

### Get Reference Data for Filters
```python
reference_data = service.get_reference_data()
equipments = reference_data['data']['equipments']
```

### Filter Exercises
```python
barbell_exercises = service.get_exercises_by_filters(
    equipment="barbell", 
    bodypart="chest", 
    limit=10
)
```

## Configuration
- API Key: Set via environment variable `EXERCISEDB_API_KEY`
- Default API Key: Included in service for testing
- Base URL: `https://exercisedb-api1.p.rapidapi.com/api/v1`

## Error Handling
All methods return a standardized response format:
```python
{
    "success": bool,
    "data": dict,  # API response data
    "message": str,  # Human-readable message
    "error": str  # Error details (if failed)
}
```

## Dependencies
- `requests==2.31.0` - HTTP client library
- `python-decouple` - Environment variable management
- `logging` - Error and info logging

## Testing
Comprehensive test suite available at `backend/tests/test_exercise_service.py`
- Tests all 8 API endpoints
- Tests enrichment functionality
- Tests filtering capabilities
- Validates error handling

Run tests: `python tests/test_exercise_service.py`

## Integration with AI Service
The ExerciseDB service is designed to work seamlessly with the AI service:
1. AI generates workout plan with exercise names
2. ExerciseDB service enriches plan with detailed exercise data
3. Frontend receives complete workout plan with instructions, images, and muscle targets

## API Response Examples

### Exercise Data Structure
```json
{
  "id": "exr_41n2hxnFMotsXTj3",
  "name": "Push-up",
  "target": "pectorals",
  "bodyPart": "chest",
  "equipment": "body weight",
  "gifUrl": "https://...",
  "instructions": ["Step 1...", "Step 2..."],
  "secondaryMuscles": ["triceps", "shoulders"]
}
```

### Reference Data Structure
```json
{
  "equipments": ["BARBELL", "DUMBBELL", "BODY WEIGHT", ...],
  "exercise_types": ["STRENGTH", "CARDIO", "STRETCHING", ...],
  "bodyparts": ["CHEST", "BACK", "SHOULDERS", ...],
  "muscles": ["PECTORALIS MAJOR", "DELTOID ANTERIOR", ...]
}
```

## Performance Notes
- All API calls include 15-second timeout
- Reference data endpoints are lightweight
- Exercise search supports pagination via limit parameter
- Enrichment process maintains high success rate (typically 100%)

## Future Enhancements
- Caching for reference data
- Batch exercise retrieval optimization  
- Exercise recommendation based on user preferences
- Integration with workout tracking features