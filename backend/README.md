# EasyFitness Backend

A Django REST API backend for the EasyFitness application - a comprehensive fitness tracking platform with full CRUD operations for user management, workout planning, exercise tracking, and nutrition logging.

## Project Structure

```
backend/
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── .env.example                # Environment variables template
├── easyfitness_env/            # Virtual environment (created during setup)
├── easyfitness_backend/        # Main Django project
│   ├── __init__.py
│   ├── settings.py             # Django settings
│   ├── urls.py                 # Main URL configuration
│   ├── wsgi.py                 # WSGI application
│   └── asgi.py                 # ASGI application
└── api/                        # Main API application
    ├── __init__.py
    ├── admin.py                # Django admin configuration
    ├── apps.py                 # App configuration
    ├── models.py               # Database models
    ├── serializers.py          # DRF serializers
    ├── urls.py                 # API URL patterns
    ├── views.py                # API views and ViewSets
    └── tests.py                # Unit tests
```

## 🚀 Quick Start Guide

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

### Installation & Setup

1. **Navigate to the backend directory:**
   ```bash
   cd /path/to/your/project/backend
   ```

2. **Virtual environment should already exist. If not, create it:**
   ```bash
   python -m venv easyfitness_env
   ```

3. **Activate the virtual environment and install dependencies:**
   ```bash
   # Activate virtual environment
   source easyfitness_env/bin/activate
   
   # Install dependencies (if needed)
   pip install -r requirements.txt
   ```

4. **Run database migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Verify the setup:**
   ```bash
   python manage.py check
   ```

## 🏃‍♂️ Starting the Server

### One-Command Start (Recommended)
```bash
cd /path/to/your/project/backend && source easyfitness_env/bin/activate && python manage.py runserver 0.0.0.0:8000
```

### Step-by-Step Start
```bash
# 1. Navigate to backend directory
cd /path/to/your/project/backend

# 2. Activate virtual environment
source easyfitness_env/bin/activate

# 3. Start the server
python manage.py runserver 0.0.0.0:8000
```

The API will be available at `http://localhost:8000/`

### Server Status
When running successfully, you should see:
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
October 12, 2025 - 20:45:52
Django version 4.2.7, using settings 'easyfitness_backend.settings'
Starting development server at http://0.0.0.0:8000/
Quit the server with CONTROL-C.
```

## 🧪 Testing the API

### Health Check
First, verify the server is running:
```bash
curl http://localhost:8000/api/health/
```
**Expected Response:**
```json
{"status":"healthy"}
```

### API Information
Get all available endpoints:
```bash
curl http://localhost:8000/api/info/ | python3 -m json.tool
```

### Complete CRUD Testing Examples

#### 1. Users API (Full CRUD)

**GET - List all users:**
```bash
curl http://localhost:8000/api/users/
```

**POST - Create a new user:**
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"username":"newuser","email":"newuser@example.com","gender":"male"}' \
  http://localhost:8000/api/users/
```

**PUT - Update a user (replace USER_ID with actual ID):**
```bash
curl -X PUT -H "Content-Type: application/json" \
  -d '{"username":"updated_user","email":"updated@example.com","gender":"female"}' \
  http://localhost:8000/api/users/USER_ID/
```

**DELETE - Remove a user:**
```bash
curl -X DELETE http://localhost:8000/api/users/USER_ID/
```

#### 2. Exercises API

**GET - List exercises:**
```bash
curl http://localhost:8000/api/exercises/
```

**POST - Create an exercise:**
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"name":"Squats","exercise_type":"strength","met_value":"5.0"}' \
  http://localhost:8000/api/exercises/
```

#### 3. Workout Plans API

**GET - List workout plans:**
```bash
curl http://localhost:8000/api/workout-plans/
```

**GET - Get workout plan with details:**
```bash
curl http://localhost:8000/api/workout-plans/PLAN_ID/with_details/
```

**GET - Get workout plans for specific user:**
```bash
curl http://localhost:8000/api/workout-plans/user/USER_ID/
```

#### 4. User Dashboard

**GET - Complete user dashboard with all related data:**
```bash
curl http://localhost:8000/api/users/USER_ID/dashboard/
```

### API Testing with Python
```python
import requests

# Base URL
BASE_URL = "http://localhost:8000/api"

# Test health endpoint
response = requests.get(f"{BASE_URL}/health/")
print(f"Health: {response.json()}")

# Create a user
user_data = {
    "username": "testuser",
    "email": "test@example.com",
    "gender": "male"
}
response = requests.post(f"{BASE_URL}/users/", json=user_data)
user = response.json()
print(f"Created user: {user}")

# Get all users
response = requests.get(f"{BASE_URL}/users/")
print(f"All users: {response.json()}")
```

## 📊 Available API Endpoints

### Base URL: `http://localhost:8000/api/`

#### Core Endpoints
| Endpoint | Methods | Description |
|----------|---------|-------------|
| `/health/` | GET | Health check |
| `/info/` | GET | API information and endpoints list |

#### User Management
| Endpoint | Methods | Description |
|----------|---------|-------------|
| `/users/` | GET, POST | List users, create user |
| `/users/{id}/` | GET, PUT, PATCH, DELETE | User details, update, delete |
| `/users/{id}/dashboard/` | GET | User dashboard with aggregated data |
| `/user-metrics/` | GET, POST | User metrics (weight, height, etc.) |
| `/goals/` | GET, POST | User fitness goals |

#### Exercise & Workout System
| Endpoint | Methods | Description |
|----------|---------|-------------|
| `/exercises/` | GET, POST | Exercise database |
| `/muscles/` | GET, POST | Muscle groups |
| `/equipment/` | GET, POST | Exercise equipment |
| `/body-parts/` | GET, POST | Body parts |
| `/workout-plans/` | GET, POST | Workout plans |
| `/workout-plans/user/{user_id}/` | GET | User's workout plans |
| `/workout-plans/{id}/with_details/` | GET | Detailed workout plan |
| `/plan-days/` | GET, POST | Individual workout days |
| `/plan-exercises/` | GET, POST | Exercises within workout days |
| `/workout-logs/` | GET, POST | Workout session logs |

#### Nutrition System
| Endpoint | Methods | Description |
|----------|---------|-------------|
| `/foods/` | GET, POST | Food database |
| `/nutrition-logs/` | GET, POST | Food consumption logs |
| `/recipes/` | GET, POST | Recipe database |
| `/ingredients/` | GET, POST | Recipe ingredients |
| `/meal-plans/` | GET, POST | Meal planning |
| `/meal-plans/user/{user_id}/` | GET | User's meal plans |
| `/meal-plans/{id}/with_details/` | GET | Detailed meal plan |

#### Relationship Tables
| Endpoint | Methods | Description |
|----------|---------|-------------|
| `/exercise-muscles/` | GET, POST | Exercise-muscle relationships |
| `/exercise-equipment/` | GET, POST | Exercise-equipment relationships |
| `/exercise-body-parts/` | GET, POST | Exercise-body part relationships |
| `/related-exercises/` | GET, POST | Related exercise suggestions |

## 🏗️ Database Models

### User Management
- **User**: Core user profile (username, email, demographics)
- **UserMetrics**: User measurements (weight, height, activity level)
- **Goal**: User fitness goals with targets and dates

### Exercise System
- **Exercise**: Exercise database with instructions and metadata
- **Muscle**: Muscle groups targeted by exercises
- **Equipment**: Equipment required for exercises
- **BodyPart**: Body parts worked by exercises
- **WorkoutPlan**: User's custom workout plans
- **PlanDay**: Individual days within workout plans
- **PlanExercise**: Exercises within workout days (sets, reps, rest)
- **WorkoutLog**: Completed workout sessions

### Nutrition System
- **Food**: Food database with nutritional information
- **NutritionLog**: User's food consumption tracking
- **Recipe**: Recipe database with instructions
- **Ingredient**: Recipe ingredients
- **MealPlan**: User's meal planning
- **MealPlanDay**: Days within meal plans
- **MealPlanEntry**: Specific meals within plan days

## 🛠️ Development

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test api

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

### Code Quality

```bash
# Format code with black
black .

# Sort imports with isort
isort .

# Lint with flake8
flake8 .
```

### Database Management

```bash
# Create new migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser

# Access Django admin at http://localhost:8000/admin/
```

### Troubleshooting

#### Common Issues

1. **Virtual Environment Not Activated:**
   ```bash
   # Make sure you see (easyfitness_env) in your terminal prompt
   source easyfitness_env/bin/activate
   ```

2. **Django Not Found:**
   ```bash
   # Ensure you're in the right directory and environment is activated
   which python3  # Should point to easyfitness_env/bin/python3
   pip list | grep Django  # Should show Django 4.2.7
   ```

3. **Database Issues:**
   ```bash
   # Reset database (development only)
   rm db.sqlite3
   python manage.py migrate
   ```

4. **Port Already in Use:**
   ```bash
   # Use a different port
   python manage.py runserver 8001
   ```

### API Development Guidelines

1. **Use Django REST Framework ViewSets** for consistent API patterns
2. **Follow RESTful conventions** for URL patterns
3. **Include proper serializers** for data validation
4. **Add comprehensive tests** for all endpoints
5. **Use UUID primary keys** for security
6. **Document API changes** in this README

## 🚀 Frontend Integration

The backend is ready for frontend integration with:

- **CORS enabled** for `http://localhost:3000` (Next.js default)
- **JSON responses** for all endpoints
- **Consistent error handling** with HTTP status codes
- **Pagination** built-in for list endpoints
- **Foreign key relationships** properly serialized

### Example Frontend Integration (JavaScript)

```javascript
// API base configuration
const API_BASE_URL = 'http://localhost:8000/api';

// Fetch user data
async function getUsers() {
    const response = await fetch(`${API_BASE_URL}/users/`);
    return response.json();
}

// Create new user
async function createUser(userData) {
    const response = await fetch(`${API_BASE_URL}/users/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData)
    });
    return response.json();
}

// Get user dashboard
async function getUserDashboard(userId) {
    const response = await fetch(`${API_BASE_URL}/users/${userId}/dashboard/`);
    return response.json();
}
```

## 📝 Environment Variables

Create a `.env` file based on `.env.example`:

```bash
# Database Configuration (optional - defaults to SQLite)
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=5432

# Security
SECRET_KEY=your-secret-key-here
DEBUG=True

# CORS
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
```

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [API Testing with Postman](https://www.postman.com/)
- [cURL Documentation](https://curl.se/docs/)

## 🎉 Success Verification

If everything is working correctly, you should be able to:

1. ✅ Start the server without errors
2. ✅ Access `http://localhost:8000/api/health/` and get `{"status":"healthy"}`
3. ✅ View all endpoints at `http://localhost:8000/api/info/`
4. ✅ Create, read, update, and delete users via the API
5. ✅ Access the Django admin at `http://localhost:8000/admin/`

The backend is now fully functional and ready for frontend integration! 🚀
