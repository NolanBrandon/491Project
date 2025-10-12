# EasyFitness API Documentation

A comprehensive guide to all available API endpoints for the EasyFitness backend.

## Base URL
```
http://localhost:8000/api/
```

## Table of Contents
1. [Health & System Endpoints](#health--system-endpoints)
2. [User Management](#user-management)
3. [User Metrics & Goals](#user-metrics--goals)
4. [Exercise System](#exercise-system)
5. [Workout Planning](#workout-planning)
6. [Workout Logging](#workout-logging)
7. [Nutrition System](#nutrition-system)
8. [Meal Planning](#meal-planning)
9. [Recipe Management](#recipe-management)
10. [Relationship Tables](#relationship-tables)
11. [Common Patterns](#common-patterns)
12. [Error Handling](#error-handling)

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

**Purpose:** Manage exercise database

#### Get All Exercises
```bash
curl http://localhost:8000/api/exercises/
```

#### Create Exercise
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "name": "Push-ups",
    "exercise_type": "strength",
    "overview": "Upper body strength exercise",
    "instructions": "Place hands on ground, lower body, push up",
    "met_value": "4.0"
  }' \
  http://localhost:8000/api/exercises/
```

**Fields:**
- `name` (String): Exercise name
- `exerciseDbId` (String): External database ID
- `exercise_type` (Choice): strength, cardio, plyometrics, stretching
- `overview` (Text): Brief description
- `instructions` (Text): Detailed instructions
- `image_url` (Text): Image URL
- `video_url` (Text): Video URL
- `met_value` (Decimal): Metabolic equivalent value

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

```bash
curl http://localhost:8000/api/workout-plans/PLAN_ID/with_details/
```

**Returns:** Complete workout plan with all days and exercises

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

#### Create Meal Plan
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "user": "6e37b248-445c-45a9-8121-a565668f5f26",
    "name": "Weekly Meal Plan",
    "description": "Balanced nutrition for the week"
  }' \
  http://localhost:8000/api/meal-plans/
```

#### Get User's Meal Plans
**Endpoint:** `GET /api/meal-plans/user/{user_id}/`

```bash
curl http://localhost:8000/api/meal-plans/user/6e37b248-445c-45a9-8121-a565668f5f26/
```

#### Get Detailed Meal Plan
**Endpoint:** `GET /api/meal-plans/{id}/with_details/`

```bash
curl http://localhost:8000/api/meal-plans/PLAN_ID/with_details/
```

### Meal Plan Days
**Endpoint:** `/api/meal-plan-days/`
**Methods:** GET, POST, PUT, PATCH, DELETE

#### Create Meal Plan Day
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "meal_plan": "MEAL_PLAN_ID",
    "day_number": 1
  }' \
  http://localhost:8000/api/meal-plan-days/
```

### Meal Plan Entries
**Endpoint:** `/api/meal-plan-entries/`
**Methods:** GET, POST, PUT, PATCH, DELETE

#### Add Food to Meal Plan
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "meal_plan_day": "MEAL_PLAN_DAY_ID",
    "food": "FOOD_ID",
    "meal_type": "breakfast"
  }' \
  http://localhost:8000/api/meal-plan-entries/
```

#### Add Recipe to Meal Plan
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "meal_plan_day": "MEAL_PLAN_DAY_ID",
    "recipe": "RECIPE_ID",
    "meal_type": "dinner"
  }' \
  http://localhost:8000/api/meal-plan-entries/
```

**Note:** Each entry must have either `food` OR `recipe`, but not both.

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

### Basic API Client Setup
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
            // Store user info in localStorage for persistence
            localStorage.setItem('currentUser', JSON.stringify(response.user));
        }
        
        return response;
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

    async createUser(userData) {
        return this.request('/users/', {
            method: 'POST',
            body: JSON.stringify(userData),
        });
    }

    async getUserDashboard(userId) {
        return this.request(`/users/${userId}/dashboard/`);
    }

    // Exercise methods
    async getExercises() {
        return this.request('/exercises/');
    }

    async createWorkoutPlan(planData) {
        return this.request('/workout-plans/', {
            method: 'POST',
            body: JSON.stringify(planData),
        });
    }

    // Nutrition methods
    async logFood(logData) {
        return this.request('/nutrition-logs/', {
            method: 'POST',
            body: JSON.stringify(logData),
        });
    }
}

// Usage Examples
const api = new EasyFitnessAPI();

// Register a new user
try {
    const newUser = await api.register({
        username: 'fitnessfan',
        email: 'fitness@example.com',
        password: 'securepass123',
        passwordConfirm: 'securepass123',
        gender: 'female',
        dateOfBirth: '1995-05-15'
    });
    console.log('User registered:', newUser);
} catch (error) {
    console.error('Registration failed:', error.message);
}

// Login
try {
    const loginResponse = await api.login('fitnessfan', 'securepass123');
    console.log('Login successful:', loginResponse);
    
    // Get user dashboard
    const dashboard = await api.getUserDashboard(loginResponse.user.id);
    console.log('Dashboard data:', dashboard);
} catch (error) {
    console.error('Login failed:', error.message);
}

// Change password
try {
    await api.changePassword(api.currentUser.id, 'securepass123', 'newsecurepass456');
    console.log('Password changed successfully');
} catch (error) {
    console.error('Password change failed:', error.message);
}
```

---

This documentation covers all available endpoints in the EasyFitness API. Each endpoint supports standard RESTful operations, and the API provides comprehensive functionality for fitness tracking, workout planning, and nutrition management.

For additional help or questions, refer to the main README.md file or contact the development team.