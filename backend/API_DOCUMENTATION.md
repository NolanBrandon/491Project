# EasyFitness API Documentation

A comprehensive guide to all available API endpoints for the EasyFitness backend.

## Base URL
```
http://localhost:8000/api/
```

## Table of Contents
1. [Health & System Endpoints](#health--system-endpoints)
2. [User Management](#user-management)
3. [AI-Powered Services](#ai-powered-services)
4. [User Metrics & Goals](#user-metrics--goals)
5. [Exercise System](#exercise-system)
6. [Workout Planning](#workout-planning)
7. [Workout Logging](#workout-logging)
8. [Nutrition System](#nutrition-system)
9. [Meal Planning](#meal-planning)
10. [Recipe Management](#recipe-management)
11. [Relationship Tables](#relationship-tables)
12. [Common Patterns](#common-patterns)
13. [Error Handling](#error-handling)

---

## Health & System Endpoints

### Health Check
**Endpoint:** `GET /api/health/`

**Purpose:** Check if the API is running properly

**Example Request:**
```bash
curl http://localhost:8000/api/health/
```

**Example Response:**
```json
{
    "status": "healthy"
}
```

### API Information
**Endpoint:** `GET /api/info/`

**Purpose:** Get list of all available endpoints

**Example Request:**
```bash
curl http://localhost:8000/api/info/
```

**Example Response:**
```json
{
    "name": "EasyFitness API",
    "version": "1.0",
    "endpoints": [
        "/health/",
        "/info/",
        "/users/",
        "..."
    ]
}
```

---

## User Management

### Users
**Endpoint:** `/api/users/`
**Methods:** GET, POST, PUT, PATCH, DELETE

#### List All Users
```bash
# GET /api/users/
curl http://localhost:8000/api/users/
```

#### Create New User (with Password)
```bash
# POST /api/users/
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123",
    "password_confirm": "securepassword123",
    "gender": "male",
    "date_of_birth": "1990-01-15"
  }' \
  http://localhost:8000/api/users/
```

**Password Requirements:**
- Minimum 8 characters
- Password and password_confirm must match
- Password is hashed and stored securely

#### User Login
**Endpoint:** `POST /api/users/login/`

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "securepassword123"
  }' \
  http://localhost:8000/api/users/login/
```

**Success Response:**
```json
{
    "message": "Login successful",
    "user": {
        "id": "uuid-here",
        "username": "johndoe",
        "email": "john@example.com",
        "gender": "male",
        "date_of_birth": "1990-01-15",
        "login_streak": 0,
        "created_at": "2025-10-12T..."
    }
}
```

#### Change Password
**Endpoint:** `POST /api/users/{id}/change_password/`

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "old_password": "oldpassword123",
    "new_password": "newsecurepassword456"
  }' \
  http://localhost:8000/api/users/6e37b248-445c-45a9-8121-a565668f5f26/change_password/
```

#### Get Specific User
```bash
# GET /api/users/{id}/
curl http://localhost:8000/api/users/6e37b248-445c-45a9-8121-a565668f5f26/
```

#### Update User Profile (No Password)
```bash
# PUT /api/users/{id}/
curl -X PUT -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe_updated",
    "email": "john.updated@example.com",
    "gender": "male",
    "date_of_birth": "1990-01-15"
  }' \
  http://localhost:8000/api/users/6e37b248-445c-45a9-8121-a565668f5f26/
```

#### Delete User
```bash
# DELETE /api/users/{id}/
curl -X DELETE http://localhost:8000/api/users/6e37b248-445c-45a9-8121-a565668f5f26/
```

#### User Dashboard
**Endpoint:** `GET /api/users/{id}/dashboard/`

**Purpose:** Get comprehensive user data including workout plans, meal plans, goals, and recent activity

```bash
curl http://localhost:8000/api/users/6e37b248-445c-45a9-8121-a565668f5f26/dashboard/
```

**Response includes:**
- User profile information
- Active workout plans
- Active meal plans
- Current goals
- Recent workout logs
- Latest metrics

---

## AI-Powered Services

### Test AI Services Status
**Endpoint:** `GET /api/test-ai-services/`

**Purpose:** Check if AI and ExerciseDB services are operational

**Example Request:**
```bash
curl http://localhost:8000/api/test-ai-services/
```

**Example Response:**
```json
{
    "ai_service": "ready",
    "exercise_service": "ready", 
    "status": "All services operational"
}
```

### Generate Enriched Workout Plan
**Endpoint:** `POST /api/generate-workout-plan/`

**Purpose:** Generate AI-powered workout plans with ExerciseDB enrichment

**Example Request:**
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "user_id": "6e37b248-445c-45a9-8121-a565668f5f26",
    "fitness_level": "advanced",
    "workout_type": "strength_hypertrophy", 
    "days_per_week": 4,
    "gender": "female",
    "equipment_preference": "gym",
    "training_experience": "2+ years",
    "specific_goals": "Build muscle mass and increase strength"
  }' \
  http://localhost:8000/api/generate-workout-plan/
```

**Request Parameters:**
- `user_id` (UUID, required): User ID
- `fitness_level` (String, required): beginner, intermediate, advanced
- `workout_type` (String, required): strength, cardio, strength_hypertrophy, functional
- `days_per_week` (Integer, required): 3-6 days
- `gender` (String, required): male, female, other
- `equipment_preference` (String, optional): gym, home, bodyweight
- `training_experience` (String, optional): Experience level description
- `specific_goals` (String, optional): Detailed goals and preferences

**Success Response:**
```json
{
    "success": true,
    "message": "Enriched workout plan generated and saved successfully",
    "saved_plan_id": "7b276838-d32b-4be4-82b7-79e6fcf35637",
    "plan_name": "Advanced 4-Day Strength & Hypertrophy Split",
    "total_days": 4,
    "total_exercises": 24,
    "ai_generation": {
        "success": true,
        "exercises_generated": 24
    },
    "enrichment": {
        "success": true,
        "exercises_enriched": 24,
        "exercises_with_images": 24,
        "exercises_with_videos": 23,
        "exercises_with_instructions": 24
    }
}
```

**Error Response:**
```json
{
    "success": false,
    "error": "AI service temporarily unavailable",
    "details": "Gemini API quota exceeded"
}
```

### AI Service Features

#### Intelligent Exercise Matching
- **ExerciseDB Integration**: 1300+ exercises with professional images and videos
- **Smart Matching**: Multiple algorithms to find best exercise matches
- **Fallback Strategies**: Graceful handling of unmatched exercises
- **Equipment-Based Filtering**: Matches exercises to available equipment

#### AI Workout Generation
- **Google Gemini Integration**: Advanced AI for personalized workout creation
- **Structured Output**: JSON-formatted workout plans with proper progression
- **Experience-Based Programming**: Different approaches for beginner/intermediate/advanced
- **Gender-Specific Considerations**: Tailored recommendations based on gender
- **Goal-Oriented Programming**: Customized for strength, hypertrophy, conditioning

### Generate AI Meal Plan
**Endpoint:** `POST /api/generate-meal-plan/`

**Purpose:** Generate AI-powered personalized meal plans with complete nutritional data

**Example Request:**
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "user_id": "9b88c628-9a89-4fc7-aeac-a90cf3f16efe",
    "daily_calorie_target": 2000,
    "dietary_preferences": ["balanced"],
    "goal": "maintain weight",
    "days_count": 3,
    "gender": "female",
    "age": 25,
    "activity_level": "moderate"
  }' \
  http://localhost:8000/api/generate-meal-plan/
```

**Request Parameters:**
- `user_id` (UUID, required): User ID
- `daily_calorie_target` (Integer, required): Target calories per day (1200-4000)
- `dietary_preferences` (Array, required): ["balanced", "low_carb", "high_protein", "vegetarian", "vegan", "keto", "mediterranean"]
- `goal` (String, required): "lose weight", "gain weight", "maintain weight", "build muscle"
- `days_count` (Integer, required): Number of days to plan (1-7)
- `gender` (String, required): "male", "female", "other"
- `age` (Integer, required): User's age (16-100)
- `activity_level` (String, required): "sedentary", "light", "moderate", "active", "very_active"

**Success Response:**
```json
{
    "success": true,
    "message": "AI meal plan generated and saved successfully",
    "saved_plan_id": "f1790f75-1ea1-429e-852c-f650e16c5262",
    "plan_name": "5-Day Balanced Weight Maintenance Meal Plan",
    "total_days": 5,
    "daily_calorie_target": 2000,
    "ai_generation": {
        "success": true,
        "days_generated": 5,
        "meals_per_day": 3
    }
}
```

**Error Response:**
```json
{
    "success": false,
    "error": "Invalid calorie target",
    "details": "Daily calorie target must be between 1200 and 4000"
}
```

#### AI Meal Plan Features
- **Nutritional Precision**: Complete macro and micronutrient breakdowns per ingredient
- **Detailed Recipes**: Ingredient measurements, prep times, and cooking instructions
- **Goal-Oriented**: Customized for weight loss, gain, maintenance, or muscle building
- **Dietary Compatibility**: Supports various dietary preferences and restrictions
- **JSON Storage**: Complete meal plan data preserved in simplified database schema
- **Flexible Duration**: Generate 1-7 day meal plans based on user needs

---

## User Metrics & Goals

### User Metrics
**Endpoint:** `/api/user-metrics/`
**Methods:** GET, POST, PUT, PATCH, DELETE

**Purpose:** Track user's physical measurements over time

#### Create User Metrics
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "user": "6e37b248-445c-45a9-8121-a565668f5f26",
    "date_recorded": "2025-10-12",
    "weight_kg": "75.5",
    "height_cm": "175.0",
    "activity_level": "active"
  }' \
  http://localhost:8000/api/user-metrics/
```

#### Get User Metrics
```bash
# All metrics
curl http://localhost:8000/api/user-metrics/

# Filter by user (add as query parameter)
curl "http://localhost:8000/api/user-metrics/?user=6e37b248-445c-45a9-8121-a565668f5f26"
```

**Fields:**
- `user` (UUID): Foreign key to User
- `date_recorded` (Date): When metrics were recorded
- `weight_kg` (Decimal): Weight in kilograms
- `height_cm` (Decimal): Height in centimeters
- `activity_level` (String): Activity level description

### Goals
**Endpoint:** `/api/goals/`
**Methods:** GET, POST, PUT, PATCH, DELETE

**Purpose:** Manage user fitness goals

#### Create Goal
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "user": "6e37b248-445c-45a9-8121-a565668f5f26",
    "goal_type": "weight_loss",
    "target_weight_kg": "70.0",
    "start_date": "2025-10-12",
    "end_date": "2026-01-12",
    "is_active": true
  }' \
  http://localhost:8000/api/goals/
```

**Fields:**
- `user` (UUID): Foreign key to User
- `goal_type` (String): Type of goal (weight_loss, muscle_gain, etc.)
- `target_weight_kg` (Decimal): Target weight
- `start_date` (Date): Goal start date
- `end_date` (Date): Goal target completion date
- `is_active` (Boolean): Whether goal is currently active

---

## Exercise System

### Exercises
**Endpoint:** `/api/exercises/`
**Methods:** GET, POST, PUT, PATCH, DELETE

**Purpose:** Manage exercise database with ExerciseDB integration

#### Get All Exercises
```bash
curl http://localhost:8000/api/exercises/
```

#### Create Exercise
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "name": "Push-ups",
    "exerciseDbId": "exr_41n2hxnFMotsXTj3",
    "exercise_type": "STRENGTH",
    "overview": "Upper body strength exercise targeting chest, shoulders, and triceps",
    "instructions": "[\"Place hands on ground shoulder-width apart\", \"Lower body until chest nearly touches ground\", \"Push up to starting position\"]",
    "image_url": "https://cdn.exercisedb.dev/w/images/example.png",
    "video_url": "https://cdn.exercisedb.dev/w/videos/example.mp4",
    "met_value": "4.0"
  }' \
  http://localhost:8000/api/exercises/
```

**Enhanced Fields:**
- `name` (String): Exercise name
- `exerciseDbId` (String): ExerciseDB external ID for enrichment
- `exercise_type` (Choice): STRENGTH, CARDIO, PLYOMETRICS, STRETCHING, WEIGHTLIFTING
- `overview` (Text): Comprehensive exercise description and benefits
- `instructions` (Text): JSON array of step-by-step instructions
- `image_url` (Text): High-quality exercise demonstration image
- `video_url` (Text): Instructional video URL
- `met_value` (Decimal): Metabolic equivalent value for calorie calculation

#### ExerciseDB Integration Features
- **1300+ Professional Exercises**: Complete database from ExerciseDB
- **28 Equipment Types**: From barbell to resistance bands
- **18 Body Parts**: Comprehensive muscle group targeting
- **High-Quality Media**: Professional images and demonstration videos
- **Detailed Instructions**: Step-by-step exercise guidance
- **Automatic Enrichment**: AI-generated workouts automatically enriched with ExerciseDB data

### Muscles
**Endpoint:** `/api/muscles/`
**Methods:** GET, POST, PUT, PATCH, DELETE

#### Create Muscle Group
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "name": "Biceps"
  }' \
  http://localhost:8000/api/muscles/
```

### Equipment
**Endpoint:** `/api/equipment/`
**Methods:** GET, POST, PUT, PATCH, DELETE

#### Create Equipment
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "name": "Dumbbells"
  }' \
  http://localhost:8000/api/equipment/
```

### Body Parts
**Endpoint:** `/api/body-parts/`
**Methods:** GET, POST, PUT, PATCH, DELETE

#### Create Body Part
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "name": "Arms"
  }' \
  http://localhost:8000/api/body-parts/
```

---

## Workout Planning

### Workout Plans
**Endpoint:** `/api/workout-plans/`
**Methods:** GET, POST, PUT, PATCH, DELETE

#### Create Workout Plan
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "user": "6e37b248-445c-45a9-8121-a565668f5f26",
    "name": "Upper Body Strength",
    "description": "3-day upper body workout plan"
  }' \
  http://localhost:8000/api/workout-plans/
```

#### Get User's Workout Plans
**Endpoint:** `GET /api/workout-plans/user/{user_id}/`

```bash
curl http://localhost:8000/api/workout-plans/user/6e37b248-445c-45a9-8121-a565668f5f26/
```

#### Get Detailed Workout Plan
**Endpoint:** `GET /api/workout-plans/{id}/with_details/`

**Purpose:** Get complete workout plan with all days, exercises, and ExerciseDB enrichment

```bash
curl http://localhost:8000/api/workout-plans/7b276838-d32b-4be4-82b7-79e6fcf35637/with_details/
```

**Example Response:**
```json
{
  "id": "7b276838-d32b-4be4-82b7-79e6fcf35637",
  "name": "Advanced 4-Day Strength & Hypertrophy Split",
  "description": "A comprehensive 4-day program for advanced female lifters...",
  "created_at": "2025-10-12T23:09:39.819563Z",
  "user": "9b88c628-9a89-4fc7-aeac-a90cf3f16efe",
  "days": [
    {
      "id": "17edabc3-1033-4696-91b5-a51e8af5f561",
      "day_number": 1,
      "name": "Upper Body - Strength Focus",
      "plan": "7b276838-d32b-4be4-82b7-79e6fcf35637",
      "exercises": [
        {
          "id": "ffe17f19-55fb-49f9-9272-c55f5b156e4a",
          "display_order": 6,
          "sets": 4,
          "reps": "4-6",
          "rest_period_seconds": null,
          "plan_day": "17edabc3-1033-4696-91b5-a51e8af5f561",
          "exercise": "84e74ed5-ecce-4acd-99aa-427566dd7aa6",
          "exercise_details": {
            "id": "84e74ed5-ecce-4acd-99aa-427566dd7aa6",
            "exerciseDbId": "exr_41n2hxnFMotsXTj3",
            "name": "Barbell Bench Press",
            "image_url": "https://cdn.exercisedb.dev/w/images/boDyoVc/41n2hxnFMotsXTj3__Barbell-Bench-Press_Chest.png",
            "video_url": "https://cdn.exercisedb.dev/w/videos/N75Uemp/41n2hxnFMotsXTj3__Barbell-Bench-Press_Chest2_.mp4",
            "overview": "The Bench Press is a classic strength training exercise...",
            "instructions": "['Grip the barbell with your hands slightly wider than shoulder-width apart...']",
            "exercise_type": "STRENGTH",
            "met_value": "1.00"
          }
        }
      ]
    }
  ]
}
```

**Returns:** Complete workout plan including:
- Plan metadata (name, description, dates)
- All plan days with day numbers and names  
- All exercises for each day with sets/reps/rest
- Complete ExerciseDB enrichment:
  - Professional exercise images
  - Instructional videos (where available)
  - Step-by-step instructions
  - Exercise overviews and benefits
  - Exercise type classification
  - MET values for calorie calculation

### Plan Days
**Endpoint:** `/api/plan-days/`
**Methods:** GET, POST, PUT, PATCH, DELETE

#### Create Plan Day
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "plan": "WORKOUT_PLAN_ID",
    "day_number": 1,
    "name": "Chest and Triceps"
  }' \
  http://localhost:8000/api/plan-days/
```

### Plan Exercises
**Endpoint:** `/api/plan-exercises/`
**Methods:** GET, POST, PUT, PATCH, DELETE

#### Add Exercise to Plan Day
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "plan_day": "PLAN_DAY_ID",
    "exercise": "EXERCISE_ID",
    "display_order": 1,
    "sets": 3,
    "reps": "8-12",
    "rest_period_seconds": 90
  }' \
  http://localhost:8000/api/plan-exercises/
```

**Fields:**
- `plan_day` (UUID): Foreign key to PlanDay
- `exercise` (UUID): Foreign key to Exercise
- `display_order` (Integer): Order in the workout
- `sets` (Integer): Number of sets
- `reps` (String): Reps (flexible format: "8-12", "AMRAP", "30s")
- `rest_period_seconds` (Integer): Rest time between sets

---

## Workout Logging

### Workout Logs
**Endpoint:** `/api/workout-logs/`
**Methods:** GET, POST, PUT, PATCH, DELETE

#### Log Completed Workout
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "user": "6e37b248-445c-45a9-8121-a565668f5f26",
    "exercise": "EXERCISE_ID",
    "sets_performed": 3,
    "reps_performed": 10,
    "duration_minutes": 45,
    "calories_burned": 250,
    "perceived_effort": 7
  }' \
  http://localhost:8000/api/workout-logs/
```

**Fields:**
- `user` (UUID): Foreign key to User
- `exercise` (UUID): Foreign key to Exercise
- `date_performed` (DateTime): Auto-set to now
- `sets_performed` (Integer): Sets completed
- `reps_performed` (Integer): Reps completed
- `duration_minutes` (Integer): Workout duration
- `calories_burned` (Integer): Estimated calories burned
- `perceived_effort` (Integer): RPE scale 1-10

---

## Nutrition System

### Foods
**Endpoint:** `/api/foods/`
**Methods:** GET, POST, PUT, PATCH, DELETE

#### Create Food Item
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "name": "Chicken Breast",
    "serving_size_g": "100.0",
    "calories": "165.0",
    "protein_g": "31.0",
    "carbohydrates_g": "0.0",
    "fat_g": "3.6"
  }' \
  http://localhost:8000/api/foods/
```

### Nutrition Logs
**Endpoint:** `/api/nutrition-logs/`
**Methods:** GET, POST, PUT, PATCH, DELETE

#### Log Food Consumption
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "user": "6e37b248-445c-45a9-8121-a565668f5f26",
    "food": "FOOD_ID",
    "date_eaten": "2025-10-12T12:30:00Z",
    "quantity": "1.5",
    "meal_type": "lunch"
  }' \
  http://localhost:8000/api/nutrition-logs/
```

**Fields:**
- `user` (UUID): Foreign key to User
- `food` (UUID): Foreign key to Food
- `date_eaten` (DateTime): When food was consumed
- `quantity` (Decimal): Multiplier of serving size
- `meal_type` (Choice): breakfast, lunch, dinner, snack

---

## Meal Planning

### Meal Plans
**Endpoint:** `/api/meal-plans/`
**Methods:** GET, POST, PUT, PATCH, DELETE

**Note:** The meal plan system uses a simplified JSON-based schema for storing complete AI-generated meal plans with full nutritional data.

#### Create Meal Plan (Manual)
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "user": "6e37b248-445c-45a9-8121-a565668f5f26",
    "name": "Weekly Meal Plan",
    "description": "Balanced nutrition for the week",
    "meal_plan_data": {},
    "daily_calorie_target": 2000,
    "days_count": 7,
    "dietary_preferences": ["balanced"],
    "goal": "maintain weight"
  }' \
  http://localhost:8000/api/meal-plans/
```

#### Get User's Meal Plans
**Endpoint:** `GET /api/meal-plans/user/{user_id}/`

```bash
curl http://localhost:8000/api/meal-plans/user/6e37b248-445c-45a9-8121-a565668f5f26/
```

#### Get Detailed Meal Plan with Full Data
**Endpoint:** `GET /api/meal-plans/{id}/`

```bash
curl http://localhost:8000/api/meal-plans/f1790f75-1ea1-429e-852c-f650e16c5262/
```

**Response includes complete meal plan data:**
```json
{
  "id": "f1790f75-1ea1-429e-852c-f650e16c5262",
  "name": "5-Day Balanced Weight Maintenance Meal Plan",
  "description": "A 5-day meal plan tailored for weight maintenance...",
  "meal_plan_data": {
    "days": [
      {
        "meals": {
          "breakfast": {
            "recipe_name": "Protein Oatmeal Bowl",
            "ingredients": [
              {
                "ingredient_name": "Rolled Oats",
                "measure": "1/2 cup",
                "calories": 150,
                "protein": 5,
                "carbs": 27,
                "fat": 3,
                "fiber": 4
              }
            ],
            "prep_time": 10,
            "total_calories": 450,
            "total_protein": 20,
            "cooking_instructions": "..."
          }
        }
      }
    ]
  },
  "daily_calorie_target": 2000,
  "days_count": 5,
  "dietary_preferences": ["balanced"],
  "goal": "maintain weight"
}
```

### Meal Plan Schema (Simplified)

The meal plan system now uses a **simplified JSON-based approach** instead of complex relational tables:

- **Before**: `MealPlan` → `MealPlanDay` → `MealPlanEntry` → `Food`/`Recipe`
- **After**: `MealPlan` with `meal_plan_data` JSONField containing complete data

**Benefits:**
- ✅ Preserves complete AI-generated nutritional data
- ✅ No data loss during complex joins
- ✅ Faster queries and simpler data management
- ✅ Full ingredient-level nutritional breakdowns
- ✅ Recipe instructions and prep times preserved

---

## Recipe Management

### Recipes
**Endpoint:** `/api/recipes/`
**Methods:** GET, POST, PUT, PATCH, DELETE

#### Create Recipe
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "name": "Grilled Chicken Salad",
    "category": "Main Course",
    "area": "Mediterranean",
    "instructions": "Grill chicken, mix with greens...",
    "image_url": "https://example.com/image.jpg"
  }' \
  http://localhost:8000/api/recipes/
```

### Ingredients
**Endpoint:** `/api/ingredients/`
**Methods:** GET, POST, PUT, PATCH, DELETE

#### Create Ingredient
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "name": "Olive Oil"
  }' \
  http://localhost:8000/api/ingredients/
```

### Recipe Ingredients
**Endpoint:** `/api/recipe-ingredients/`
**Methods:** GET, POST, PUT, PATCH, DELETE

#### Add Ingredient to Recipe
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "recipe": "RECIPE_ID",
    "ingredient": "INGREDIENT_ID",
    "measure": "2 tbsp"
  }' \
  http://localhost:8000/api/recipe-ingredients/
```

### Tags
**Endpoint:** `/api/tags/`
**Methods:** GET, POST, PUT, PATCH, DELETE

#### Create Tag
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "tag": "Healthy"
  }' \
  http://localhost:8000/api/tags/
```

### Recipe Tags
**Endpoint:** `/api/recipe-tags/`
**Methods:** GET, POST, PUT, PATCH, DELETE

#### Tag a Recipe
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "recipe": "RECIPE_ID",
    "tag": "TAG_ID"
  }' \
  http://localhost:8000/api/recipe-tags/
```

---

## Relationship Tables

### Exercise-Muscle Relationships
**Endpoint:** `/api/exercise-muscles/`

#### Link Exercise to Muscle
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "exercise": "EXERCISE_ID",
    "muscle": "MUSCLE_ID",
    "muscle_type": "primary"
  }' \
  http://localhost:8000/api/exercise-muscles/
```

**muscle_type options:** primary, secondary, stabilizer

### Exercise-Equipment Relationships
**Endpoint:** `/api/exercise-equipment/`

#### Link Exercise to Equipment
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "exercise": "EXERCISE_ID",
    "equipment": "EQUIPMENT_ID"
  }' \
  http://localhost:8000/api/exercise-equipment/
```

### Exercise-Body Part Relationships
**Endpoint:** `/api/exercise-body-parts/`

#### Link Exercise to Body Part
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "exercise": "EXERCISE_ID",
    "body_part": "BODY_PART_ID"
  }' \
  http://localhost:8000/api/exercise-body-parts/
```

### Keywords
**Endpoint:** `/api/keywords/`

#### Create Keyword
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "keyword": "upper body"
  }' \
  http://localhost:8000/api/keywords/
```

### Exercise Keywords
**Endpoint:** `/api/exercise-keywords/`

#### Tag Exercise with Keyword
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "exercise": "EXERCISE_ID",
    "keyword": "KEYWORD_ID"
  }' \
  http://localhost:8000/api/exercise-keywords/
```

### Related Exercises
**Endpoint:** `/api/related-exercises/`

#### Link Related Exercises
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "exercise": "EXERCISE_ID",
    "related_exercise": "RELATED_EXERCISE_ID"
  }' \
  http://localhost:8000/api/related-exercises/
```

---

## Common Patterns

### Pagination
All list endpoints return paginated results:

```json
{
    "count": 100,
    "next": "http://localhost:8000/api/users/?page=2",
    "previous": null,
    "results": [...]
}
```

### Filtering
Many endpoints support filtering via query parameters:

```bash
# Filter users by gender
curl "http://localhost:8000/api/users/?gender=male"

# Filter exercises by type
curl "http://localhost:8000/api/exercises/?exercise_type=strength"

# Filter nutrition logs by user
curl "http://localhost:8000/api/nutrition-logs/?user=USER_ID"
```

### Ordering
Use the `ordering` parameter to sort results:

```bash
# Order users by creation date (newest first)
curl "http://localhost:8000/api/users/?ordering=-created_at"

# Order exercises by name
curl "http://localhost:8000/api/exercises/?ordering=name"
```

---

## Error Handling

### HTTP Status Codes

- **200 OK**: Successful GET, PUT, PATCH
- **201 Created**: Successful POST
- **204 No Content**: Successful DELETE
- **400 Bad Request**: Invalid data provided
- **404 Not Found**: Resource doesn't exist
- **500 Internal Server Error**: Server error

### Error Response Format
```json
{
    "detail": "Not found.",
    "field_errors": {
        "email": ["This field is required."],
        "username": ["A user with that username already exists."]
    }
}
```

### Common Error Scenarios

1. **Missing Required Fields**
   ```json
   {
       "username": ["This field is required."],
       "email": ["This field is required."]
   }
   ```

2. **Unique Constraint Violations**
   ```json
   {
       "username": ["A user with that username already exists."]
   }
   ```

3. **Invalid Foreign Key References**
   ```json
   {
       "user": ["Invalid pk \"invalid-uuid\" - object does not exist."]
   }
   ```

4. **Invalid Choice Values**
   ```json
   {
       "exercise_type": ["\"invalid_type\" is not a valid choice."]
   }
   ```

---

## JavaScript Frontend Examples

### Enhanced API Client with AI Features
```javascript
const API_BASE_URL = 'http://localhost:8000/api';

class EasyFitnessAPI {
    constructor() {
        this.currentUser = null;
    }

    async request(endpoint, options = {}) {
        const url = `${API_BASE_URL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers,
            },
            ...options,
        };

        const response = await fetch(url, config);
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }
        
        return response.json();
    }

    // AI Service Methods
    async testAIServices() {
        return this.request('/test-ai-services/');
    }

    async generateWorkoutPlan(planRequest) {
        return this.request('/generate-workout-plan/', {
            method: 'POST',
            body: JSON.stringify(planRequest),
        });
    }

    async getDetailedWorkoutPlan(planId) {
        return this.request(`/workout-plans/${planId}/with_details/`);
    }

    // Authentication methods
    async register(userData) {
        const response = await this.request('/users/', {
            method: 'POST',
            body: JSON.stringify({
                username: userData.username,
                email: userData.email,
                password: userData.password,
                password_confirm: userData.passwordConfirm,
                gender: userData.gender,
                date_of_birth: userData.dateOfBirth
            }),
        });
        return response;
    }

    async login(username, password) {
        const response = await this.request('/users/login/', {
            method: 'POST',
            body: JSON.stringify({ username, password }),
        });
        
        if (response.user) {
            this.currentUser = response.user;
            localStorage.setItem('currentUser', JSON.stringify(response.user));
        }
        
        return response;
    }

    async logout() {
        try {
            const response = await this.request('/users/logout/', {
                method: 'POST',
            });
            this.currentUser = null;
            localStorage.removeItem('currentUser');
            return response;
        } catch (error) {
            // Even if logout fails on server, clear local data
            this.currentUser = null;
            localStorage.removeItem('currentUser');
            throw error;
        }
    }

    async changePassword(userId, oldPassword, newPassword) {
        return this.request(`/users/${userId}/change_password/`, {
            method: 'POST',
            body: JSON.stringify({
                old_password: oldPassword,
                new_password: newPassword
            }),
        });
    }

    // User methods
    async getUsers() {
        return this.request('/users/');
    }

    async getUserDashboard(userId) {
        return this.request(`/users/${userId}/dashboard/`);
    }

    // Exercise methods
    async getExercises() {
        return this.request('/exercises/');
    }

    async getWorkoutPlans(userId) {
        return this.request(`/workout-plans/user/${userId}/`);
    }

    // Nutrition methods
    async logFood(logData) {
        return this.request('/nutrition-logs/', {
            method: 'POST',
            body: JSON.stringify(logData),
        });
    }
}

// Advanced Usage Examples
const api = new EasyFitnessAPI();

// Complete AI Workout Generation Flow
async function generatePersonalizedWorkout() {
    try {
        // First, check if AI services are ready
        const serviceStatus = await api.testAIServices();
        console.log('AI Services Status:', serviceStatus);
        
        if (serviceStatus.ai_service !== 'ready' || serviceStatus.exercise_service !== 'ready') {
            throw new Error('AI services are not available');
        }

        // Generate AI-powered workout plan
        const workoutRequest = {
            user_id: api.currentUser.id,
            fitness_level: 'intermediate',
            workout_type: 'strength_hypertrophy',
            days_per_week: 4,
            gender: 'female',
            equipment_preference: 'gym',
            training_experience: '1-2 years of consistent training',
            specific_goals: 'Build lean muscle mass, improve strength in compound movements, and enhance overall physique'
        };

        console.log('Generating workout plan...');
        const generationResult = await api.generateWorkoutPlan(workoutRequest);
        
        if (!generationResult.success) {
            throw new Error(generationResult.error);
        }

        console.log('Workout Plan Generated Successfully!');
        console.log(`Plan ID: ${generationResult.saved_plan_id}`);
        console.log(`Plan Name: ${generationResult.plan_name}`);
        console.log(`Total Days: ${generationResult.total_days}`);
        console.log(`Total Exercises: ${generationResult.total_exercises}`);

        // Get detailed workout plan with ExerciseDB enrichment
        const detailedPlan = await api.getDetailedWorkoutPlan(generationResult.saved_plan_id);
        
        console.log('Detailed Plan Retrieved:');
        console.log(`Description: ${detailedPlan.description}`);
        
        // Display workout structure
        detailedPlan.days.forEach((day, index) => {
            console.log(`\nDay ${day.day_number}: ${day.name}`);
            console.log(`Exercises (${day.exercises.length}):`);
            
            day.exercises.forEach((exercise, exerciseIndex) => {
                const details = exercise.exercise_details;
                console.log(`  ${exerciseIndex + 1}. ${details.name}`);
                console.log(`     Sets: ${exercise.sets}, Reps: ${exercise.reps}`);
                console.log(`     Type: ${details.exercise_type}`);
                console.log(`     Image: ${details.image_url ? 'Available' : 'None'}`);
                console.log(`     Video: ${details.video_url ? 'Available' : 'None'}`);
            });
        });

        return detailedPlan;

    } catch (error) {
        console.error('Error generating workout:', error.message);
        throw error;
    }
}

// User Registration and Authentication Flow
async function registerAndLogin() {
    try {
        // Register new user
        const newUser = await api.register({
            username: 'fitnessenthusiast',
            email: 'fitness@example.com',
            password: 'SecurePass123!',
            passwordConfirm: 'SecurePass123!',
            gender: 'female',
            dateOfBirth: '1995-08-20'
        });
        console.log('User registered successfully:', newUser);

        // Login with new credentials
        const loginResponse = await api.login('fitnessenthusiast', 'SecurePass123!');
        console.log('Login successful:', loginResponse.message);
        
        // Get user dashboard
        const dashboard = await api.getUserDashboard(loginResponse.user.id);
        console.log('Dashboard loaded:', dashboard);

        return loginResponse.user;

    } catch (error) {
        console.error('Registration/Login failed:', error.message);
        throw error;
    }
}

// Workout Plan Management
async function manageWorkoutPlans(userId) {
    try {
        // Get user's existing workout plans
        const existingPlans = await api.getWorkoutPlans(userId);
        console.log(`Found ${existingPlans.length} existing workout plans`);

        // Display existing plans
        existingPlans.forEach((plan, index) => {
            console.log(`${index + 1}. ${plan.name} (Created: ${plan.created_at})`);
        });

        return existingPlans;

    } catch (error) {
        console.error('Error managing workout plans:', error.message);
        throw error;
    }
}

// Complete Application Flow Example
async function fullApplicationDemo() {
    try {
        console.log('=== EasyFitness API Demo ===\n');

        // Step 1: Register and login
        console.log('1. User Registration and Login...');
        const user = await registerAndLogin();
        
        // Step 2: Generate AI workout plan
        console.log('\n2. Generating AI-Powered Workout Plan...');
        const workoutPlan = await generatePersonalizedWorkout();
        
        // Step 3: Manage existing plans
        console.log('\n3. Managing Workout Plans...');
        const allPlans = await manageWorkoutPlans(user.id);
        
        // Step 4: Change password
        console.log('\n4. Updating Password...');
        await api.changePassword(user.id, 'SecurePass123!', 'NewSecurePass456!');
        console.log('Password updated successfully');
        
        // Step 5: Logout
        console.log('\n5. Logging Out...');
        await api.logout();
        console.log('Logout successful');

        console.log('\n=== Demo Complete ===');
        return {
            user,
            workoutPlan,
            allPlans
        };

    } catch (error) {
        console.error('Demo failed:', error.message);
        throw error;
    }
}

// Error Handling Examples
api.generateWorkoutPlan({
    user_id: 'invalid-id',
    fitness_level: 'beginner',
    workout_type: 'strength',
    days_per_week: 3,
    gender: 'male'
}).catch(error => {
    if (error.message.includes('Invalid pk')) {
        console.error('Invalid user ID provided');
    } else if (error.message.includes('AI service')) {
        console.error('AI service is temporarily unavailable');
    } else {
        console.error('Unexpected error:', error.message);
    }
});

// Frontend Integration with React/Next.js
const WorkoutPlanGenerator = () => {
    const [loading, setLoading] = useState(false);
    const [workoutPlan, setWorkoutPlan] = useState(null);
    const [error, setError] = useState(null);

    const generateWorkout = async (formData) => {
        setLoading(true);
        setError(null);
        
        try {
            const result = await api.generateWorkoutPlan({
                user_id: formData.userId,
                fitness_level: formData.fitnessLevel,
                workout_type: formData.workoutType,
                days_per_week: parseInt(formData.daysPerWeek),
                gender: formData.gender,
                equipment_preference: formData.equipment,
                specific_goals: formData.goals
            });

            if (result.success) {
                const detailedPlan = await api.getDetailedWorkoutPlan(result.saved_plan_id);
                setWorkoutPlan(detailedPlan);
            }
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            {loading && <p>Generating your personalized workout plan...</p>}
            {error && <p className="error">Error: {error}</p>}
            {workoutPlan && (
                <div>
                    <h2>{workoutPlan.name}</h2>
                    <p>{workoutPlan.description}</p>
                    {/* Render workout days and exercises */}
                </div>
            )}
        </div>
    );
};
```

---

## System Architecture & Integration

### AI-Powered Workout Generation Pipeline

```
Frontend Request → Django API → AI Service → ExerciseDB API → Database → Enriched Response
```

#### 1. AI Generation (Google Gemini)
- **Input**: User preferences, fitness level, goals, equipment
- **Processing**: Advanced AI analysis and workout programming
- **Output**: Structured JSON workout plan with exercise names

#### 2. ExerciseDB Enrichment
- **Input**: Exercise names from AI generation
- **Processing**: Intelligent matching algorithms with fallback strategies
- **Output**: Professional images, videos, instructions, and metadata

#### 3. Database Persistence
- **Input**: Enriched workout plan data
- **Processing**: Relational database storage with foreign keys
- **Output**: Saved workout plan with generated UUID

#### 4. Frontend Integration
- **Input**: Generated plan ID
- **Processing**: REST API calls with CORS support
- **Output**: Complete workout plan ready for UI rendering

### Service Dependencies

#### Required Environment Variables
```bash
# Google Gemini AI
GEMINI_API_KEY=your_gemini_api_key_here

# ExerciseDB API
EXERCISEDB_API_KEY=your_exercisedb_api_key_here

# Database (Supabase/PostgreSQL)
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=your_database_host
DB_PORT=5432
```

#### CORS Configuration
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",    # Next.js development
    "http://127.0.0.1:3000",    # Alternative localhost
    "https://your-production-domain.com"  # Production frontend
]
```

#### API Rate Limits
- **Gemini AI**: Based on Google API quotas
- **ExerciseDB**: 100 requests per minute (free tier)
- **Django**: No built-in limits (configure as needed)

### Error Handling & Resilience

#### AI Service Fallbacks
1. **Gemini API Unavailable**: Return cached workout templates
2. **ExerciseDB API Down**: Use basic exercise data without enrichment
3. **Database Issues**: Return error with retry suggestions
4. **Network Timeouts**: Implement request timeouts and retries

#### Monitoring & Health Checks
- **GET /api/health/**: Basic API health status
- **GET /api/test-ai-services/**: AI and ExerciseDB service status
- **Database Connection**: Automatic connection pooling and retry

---

This documentation covers all available endpoints in the EasyFitness API. The system provides comprehensive functionality for fitness tracking, AI-powered workout planning, and nutrition management with professional exercise enrichment through ExerciseDB integration.

For additional help or questions, refer to the main README.md file or contact the development team.