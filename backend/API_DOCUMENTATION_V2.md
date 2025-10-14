# EasyFitness API Documentation v2.0

**Streamlined AI-Optimized API for Modern Fitness Applications**

## Overview

The EasyFitness API has been completely redesigned with a focus on:
- **AI-First Architecture**: Optimized for AI-generated workout and meal plans
- **JSON-Based Storage**: Simplified data structures for complex AI content
- **Minimal Database Schema**: Reduced from 17+ tables to 7 core tables
- **Frontend-Ready**: Clean, consistent endpoints perfect for modern web/mobile apps

---

## Base URL
```
http://localhost:8000/api/
```

## Quick Reference

### Core Endpoints
| Endpoint | Purpose |
|----------|---------|
| `GET /health/` | Health check |
| `GET /info/` | API information |
| `POST /users/` | User registration |
| `POST /users/login/` | User authentication |
| `GET /users/{id}/dashboard/` | User dashboard |
| `POST /generate-workout-plan/` | AI workout generation |
| `POST /generate-meal-plan/` | AI meal plan generation |

### Data Management
| Endpoint | Purpose |
|----------|---------|
| `/users/` | User management |
| `/user-metrics/` | Physical metrics tracking |
| `/goals/` | Fitness goals |
| `/workout-plans/` | AI-generated workout plans |
| `/workout-logs/` | Exercise tracking |
| `/nutrition-logs/` | Food logging |
| `/meal-plans/` | AI-generated meal plans |

---

## 🚀 Quick Start

### 1. Register a New User
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "username": "fitnessuser",
    "email": "user@example.com",
    "password": "SecurePass123",
    "password_confirm": "SecurePass123",
    "gender": "female",
    "date_of_birth": "1995-06-15"
  }' \
  http://localhost:8000/api/users/
```

### 2. Generate AI Workout Plan
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "user_id": "9b88c628-9a89-4fc7-aeac-a90cf3f16efe",
    "user_goal": "build muscle",
    "experience_level": "intermediate", 
    "days_per_week": 4,
    "save_plan": true
  }' \
  http://localhost:8000/api/generate-workout-plan/
```

### 3. Generate AI Meal Plan
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "user_id": "9b88c628-9a89-4fc7-aeac-a90cf3f16efe",
    "daily_calorie_target": 2000,
    "dietary_preferences": ["balanced"],
    "goal": "maintain weight",
    "days_count": 5,
    "gender": "female",
    "age": 25,
    "activity_level": "moderate"
  }' \
  http://localhost:8000/api/generate-meal-plan/
```

---

## 📋 Core Endpoints

### Health & System

#### Health Check
```bash
GET /api/health/
```
**Response:**
```json
{
    "status": "healthy"
}
```

#### API Information
```bash
GET /api/info/
```
**Response:**
```json
{
    "name": "EasyFitness API",
    "version": "1.0",
    "endpoints": [
        "/health/",
        "/info/",
        "/users/",
        "/users/{id}/dashboard/",
        "/user-metrics/",
        "/goals/",
        "/workout-plans/",
        "/workout-plans/user/{user_id}/",
        "/workout-logs/",
        "/nutrition-logs/",
        "/meal-plans/",
        "/meal-plans/user/{user_id}/",
        "/generate-meal-plan/",
        "/generate-workout-plan/"
    ]
}
```

---

## 👤 User Management

### Register User
```bash
POST /api/users/
```
**Request Body:**
```json
{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "SecurePass123",
    "password_confirm": "SecurePass123",
    "gender": "male",
    "date_of_birth": "1990-01-15"
}
```

### User Login
```bash
POST /api/users/login/
```
**Request Body:**
```json
{
    "username": "johndoe",
    "password": "SecurePass123"
}
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
        "date_of_birth": "1990-01-15"
    }
}
```

### User Dashboard
```bash
GET /api/users/{id}/dashboard/
```
Returns comprehensive user data including workout plans, meal plans, goals, and recent activity.

---

## 🤖 AI-Powered Services

### Test AI Services
```bash
GET /api/test-ai-services/
```
Check if AI and ExerciseDB services are operational.

### Generate Workout Plan
```bash
POST /api/generate-workout-plan/
```

**Request Parameters:**
- `user_id` (UUID, required)
- `user_goal` (String, required): "build muscle", "lose weight", "improve endurance"
- `experience_level` (String, required): "beginner", "intermediate", "advanced"
- `days_per_week` (Integer, required): 3-6 days
- `save_plan` (Boolean, optional): Save to database (default: false)

**Success Response:**
```json
{
    "success": true,
    "message": "Enriched workout plan generated and saved successfully",
    "saved_plan_id": "7b276838-d32b-4be4-82b7-79e6fcf35637",
    "plan_name": "4-Day Intermediate Muscle Building Program",
    "total_days": 4,
    "ai_generation": {
        "success": true,
        "exercises_generated": 24
    },
    "enrichment": {
        "success": true,
        "exercises_enriched": 24,
        "exercises_with_images": 24,
        "exercises_with_videos": 23
    }
}
```

### Generate Meal Plan
```bash
POST /api/generate-meal-plan/
```

**Request Parameters:**
- `user_id` (UUID, required)
- `daily_calorie_target` (Integer, required): 1200-4000
- `dietary_preferences` (Array, required): ["balanced", "low_carb", "high_protein", "vegetarian", "vegan", "keto"]
- `goal` (String, required): "lose weight", "gain weight", "maintain weight", "build muscle"
- `days_count` (Integer, required): 1-7 days
- `gender` (String, required): "male", "female", "other"
- `age` (Integer, required): 16-100
- `activity_level` (String, required): "sedentary", "light", "moderate", "active", "very_active"

**Success Response:**
```json
{
    "success": true,
    "message": "AI meal plan generated and saved successfully",
    "saved_plan_id": "f1790f75-1ea1-429e-852c-f650e16c5262",
    "plan_name": "5-Day Balanced Weight Maintenance Meal Plan",
    "total_days": 5,
    "daily_calorie_target": 2000
}
```

---

## 🏋️ Workout Management

### Workout Plans
```bash
GET /api/workout-plans/
POST /api/workout-plans/
GET /api/workout-plans/{id}/
PUT /api/workout-plans/{id}/
DELETE /api/workout-plans/{id}/
```

#### Get User's Workout Plans
```bash
GET /api/workout-plans/user/{user_id}/
```

#### Create Manual Workout Plan
```bash
POST /api/workout-plans/
```
**Request Body:**
```json
{
    "user": "9b88c628-9a89-4fc7-aeac-a90cf3f16efe",
    "name": "Custom Upper Body Routine",
    "description": "My personal upper body workout",
    "workout_plan_data": {
        "days": [
            {
                "day_number": 1,
                "name": "Chest & Triceps",
                "exercises": [
                    {
                        "name": "Bench Press",
                        "sets": 4,
                        "reps": "8-10",
                        "rest_seconds": 120
                    }
                ]
            }
        ]
    }
}
```

### Workout Logs
```bash
GET /api/workout-logs/
POST /api/workout-logs/
```

#### Log Completed Exercise
```bash
POST /api/workout-logs/
```
**Request Body:**
```json
{
    "user": "9b88c628-9a89-4fc7-aeac-a90cf3f16efe",
    "exercise_name": "Bench Press",
    "exercise_data": {
        "equipment": "barbell",
        "muscle_groups": ["chest", "triceps"],
        "instructions": ["Lie on bench", "Lower bar to chest", "Press up"]
    },
    "sets_performed": 4,
    "reps_performed": 8,
    "duration_minutes": 25,
    "calories_burned": 150,
    "perceived_effort": 7
}
```

---

## 🥗 Nutrition Management

### Nutrition Logs
```bash
GET /api/nutrition-logs/
POST /api/nutrition-logs/
```

#### Log Food Consumption
```bash
POST /api/nutrition-logs/
```
**Request Body:**
```json
{
    "user": "9b88c628-9a89-4fc7-aeac-a90cf3f16efe",
    "food_name": "Grilled Chicken Breast",
    "food_data": {
        "serving_size_g": 100,
        "calories": 165,
        "protein_g": 31,
        "carbs_g": 0,
        "fat_g": 3.6,
        "fiber_g": 0
    },
    "date_eaten": "2025-10-13T12:30:00Z",
    "quantity": 1.5,
    "meal_type": "lunch"
}
```

### Meal Plans
```bash
GET /api/meal-plans/
POST /api/meal-plans/
GET /api/meal-plans/{id}/
```

#### Get User's Meal Plans
```bash
GET /api/meal-plans/user/{user_id}/
```

#### Get Detailed Meal Plan
```bash
GET /api/meal-plans/{id}/
```
Returns complete meal plan with all days, meals, recipes, ingredients, and nutritional data.

---

## 📊 User Metrics & Goals

### User Metrics
```bash
GET /api/user-metrics/
POST /api/user-metrics/
```

#### Create User Metrics
```json
{
    "user": "9b88c628-9a89-4fc7-aeac-a90cf3f16efe",
    "date_recorded": "2025-10-13",
    "weight_kg": 75.5,
    "height_cm": 175.0,
    "activity_level": "moderate"
}
```

### Goals
```bash
GET /api/goals/
POST /api/goals/
```

#### Create Goal
```json
{
    "user": "9b88c628-9a89-4fc7-aeac-a90cf3f16efe",
    "goal_type": "weight_loss",
    "target_weight_kg": 70.0,
    "start_date": "2025-10-13",
    "end_date": "2026-01-13",
    "is_active": true
}
```

---

## 🎯 Data Architecture

### Simplified Schema

The API uses a **streamlined 7-table architecture** optimized for AI-generated content:

1. **`users`** - User management and authentication
2. **`user_metrics`** - Physical measurements and activity levels
3. **`goals`** - Fitness and health goals
4. **`workout_plans`** - AI-generated workout plans (JSON storage)
5. **`workout_logs`** - Exercise tracking with flexible data
6. **`nutrition_logs`** - Food logging with custom nutritional data
7. **`meal_plans`** - AI-generated meal plans (JSON storage)

### JSON-Based Storage Benefits

**Workout Plans & Meal Plans** use JSON storage for:
- ✅ **Complete Data Preservation**: No data loss from AI generation
- ✅ **Flexible Schema**: Accommodate varying AI output structures
- ✅ **Rich Content**: Full exercise instructions, images, videos, nutritional breakdowns
- ✅ **Performance**: Faster queries without complex joins
- ✅ **Simplicity**: Easier frontend integration and data manipulation

### Example JSON Structure

**Workout Plan Data:**
```json
{
    "plan_overview": "4-day upper/lower split for intermediate lifters",
    "total_days": 4,
    "estimated_duration_weeks": 8,
    "days": [
        {
            "day_number": 1,
            "name": "Upper Body - Push Focus",
            "exercises": [
                {
                    "name": "Barbell Bench Press",
                    "sets": 4,
                    "reps": "6-8",
                    "rest_seconds": 120,
                    "exercise_data": {
                        "exercise_id": "exr_41n2hxnFMotsXTj3",
                        "equipment": ["barbell"],
                        "muscle_groups": ["chest", "triceps", "front_delts"],
                        "instructions": ["Step 1...", "Step 2..."],
                        "image_url": "https://...",
                        "video_url": "https://..."
                    }
                }
            ]
        }
    ]
}
```

**Meal Plan Data:**
```json
{
    "plan_overview": "5-day balanced nutrition for weight maintenance",
    "total_days": 5,
    "daily_targets": {
        "calories": 2000,
        "protein_g": 150,
        "carbs_g": 200,
        "fat_g": 67
    },
    "days": [
        {
            "day_number": 1,
            "meals": {
                "breakfast": {
                    "recipe_name": "Protein Oatmeal Bowl",
                    "prep_time_minutes": 10,
                    "ingredients": [
                        {
                            "name": "Rolled Oats",
                            "amount": "1/2 cup",
                            "calories": 150,
                            "protein_g": 5,
                            "carbs_g": 27,
                            "fat_g": 3
                        }
                    ],
                    "instructions": ["Step 1...", "Step 2..."],
                    "totals": {
                        "calories": 450,
                        "protein_g": 20,
                        "carbs_g": 45,
                        "fat_g": 15
                    }
                }
            }
        }
    ]
}
```

---

## 🔧 Common Patterns

### Pagination
All list endpoints support pagination:
```json
{
    "count": 100,
    "next": "http://localhost:8000/api/users/?page=2",
    "previous": null,
    "results": [...]
}
```

### Filtering
Filter by query parameters:
```bash
# Filter by user
GET /api/workout-logs/?user=9b88c628-9a89-4fc7-aeac-a90cf3f16efe

# Filter by date range
GET /api/nutrition-logs/?date_eaten__gte=2025-10-01

# Filter by goal type
GET /api/goals/?goal_type=weight_loss&is_active=true
```

### Ordering
Sort results using `ordering` parameter:
```bash
# Newest first
GET /api/workout-plans/?ordering=-created_at

# By name
GET /api/users/?ordering=username
```

---

## ⚠️ Error Handling

### HTTP Status Codes
- **200 OK**: Successful GET, PUT, PATCH
- **201 Created**: Successful POST
- **204 No Content**: Successful DELETE
- **400 Bad Request**: Invalid data
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server error

### Error Response Format
```json
{
    "error": "Validation failed",
    "details": {
        "username": ["This field is required."],
        "email": ["Enter a valid email address."]
    }
}
```

### AI Service Errors
```json
{
    "success": false,
    "error": "AI service temporarily unavailable",
    "details": "Gemini API quota exceeded. Please try again later."
}
```

---

## 🚀 Frontend Integration

### JavaScript API Client Example
```javascript
class EasyFitnessAPI {
    constructor(baseURL = 'http://localhost:8000/api') {
        this.baseURL = baseURL;
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: { 'Content-Type': 'application/json' },
            ...options,
        };

        const response = await fetch(url, config);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    }

    // AI Services
    async generateWorkoutPlan(planData) {
        return this.request('/generate-workout-plan/', {
            method: 'POST',
            body: JSON.stringify(planData)
        });
    }

    async generateMealPlan(planData) {
        return this.request('/generate-meal-plan/', {
            method: 'POST',
            body: JSON.stringify(planData)
        });
    }

    // User Management
    async register(userData) {
        return this.request('/users/', {
            method: 'POST',
            body: JSON.stringify(userData)
        });
    }

    async login(username, password) {
        return this.request('/users/login/', {
            method: 'POST',
            body: JSON.stringify({ username, password })
        });
    }

    // Data Retrieval
    async getUserWorkoutPlans(userId) {
        return this.request(`/workout-plans/user/${userId}/`);
    }

    async getUserMealPlans(userId) {
        return this.request(`/meal-plans/user/${userId}/`);
    }

    async getUserDashboard(userId) {
        return this.request(`/users/${userId}/dashboard/`);
    }
}

// Usage Example
const api = new EasyFitnessAPI();

// Generate AI workout plan
const workoutPlan = await api.generateWorkoutPlan({
    user_id: "9b88c628-9a89-4fc7-aeac-a90cf3f16efe",
    user_goal: "build muscle",
    experience_level: "intermediate",
    days_per_week: 4,
    save_plan: true
});

console.log(`Generated: ${workoutPlan.plan_name}`);
```

---

## 📈 Performance & Scalability

### Optimizations
- **JSON Storage**: Eliminates complex JOIN queries
- **Minimal Schema**: Faster database operations
- **AI Caching**: Cached responses for common requests
- **External Services**: ExerciseDB for exercise data, reducing database size

### Recommended Usage
- **Workout Generation**: 1-2 plans per user per week
- **Meal Planning**: 1-2 plans per user per week  
- **Logging**: Unlimited exercise and nutrition logs
- **API Calls**: No built-in rate limiting (configure as needed)

---

## 🔒 Security

### Authentication
- Password hashing with salt
- Session-based authentication
- CORS configuration for frontend domains

### Data Validation
- Input sanitization on all endpoints
- UUID validation for foreign keys
- Email format validation
- Password strength requirements

### API Security
- Request size limits
- SQL injection protection via Django ORM
- XSS protection with proper JSON serialization

---

## 🌟 What's New in v2.0

### Removed (Simplified)
- ❌ **Exercise metadata system** (10+ tables eliminated)
- ❌ **Food database table** (simplified nutrition logging)
- ❌ **Complex recipe management** (AI meal plans include everything)
- ❌ **Junction tables** (exercise-muscle, exercise-equipment, etc.)

### Enhanced
- ✅ **AI-first architecture** with complete data preservation
- ✅ **JSON-based storage** for workout and meal plans
- ✅ **Streamlined endpoints** (14 core endpoints vs 25+ previously)
- ✅ **Flexible nutrition logging** with custom food data
- ✅ **ExerciseDB integration** for professional exercise content
- ✅ **Better error handling** and response consistency

### Performance Improvements
- 🚀 **60% fewer database tables** (7 vs 17+)
- 🚀 **Faster queries** with JSON storage
- 🚀 **Simpler data relationships** 
- 🚀 **Reduced API complexity**

---

The EasyFitness API v2.0 represents a complete architectural evolution focused on AI-generated content, simplified data management, and optimal frontend integration. The streamlined design eliminates complexity while preserving all the rich functionality needed for modern fitness applications.

For questions or support, refer to the main project repository or contact the development team.