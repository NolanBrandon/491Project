# EasyFitness Backend

A Django REST API backend for the EasyFitness application - a comprehensive fitness tracking platform.

## Project Structure

```
backend/
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── .env.example                # Environment variables template
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
    ├── urls.py                 # API URL patterns
    ├── views.py                # API views
    └── tests.py                # Unit tests
```

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd ../backend
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Create virtual environment
   python -m venv easyfitness_env
   
   # Activate virtual environment
   # On macOS/Linux:
   source easyfitness_env/bin/activate
   
   # On Windows:
   easyfitness_env\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env file with your settings (optional for development)
   ```

5. **Run database migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000/`

## API Endpoints

### Base URL: `http://localhost:8000/api/`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health/` | GET | Health check endpoint |
| `/api/info/` | GET | API information |
| `/admin/` | GET | Django admin interface |

### Example Responses

**Health Check (`GET /api/health/`):**
```json
{
    "status": "healthy",
    "message": "EasyFitness API is running successfully!",
    "version": "1.0.0"
}
```

**API Info (`GET /api/info/`):**
```json
{
    "name": "EasyFitness API",
    "version": "1.0.0",
    "description": "Backend API for the EasyFitness application",
    "endpoints": {
        "health": "/api/health/",
        "info": "/api/info/",
        "admin": "/admin/"
    }
}
```

## Development

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

### Formatting

```bash
# Format code with black
black .

# Sort imports with isort
isort .

# Lint with flake8
flake8 .
```

### Example Model Structure

The `api/models.py` file contains commented examples of potential models:

- User profiles
- Workout plans
- Exercises
- Workout sessions
- Calorie tracking

### API Development Guidelines

1. **Use Django REST Framework** for API endpoints
2. **Follow RESTful conventions** for URL patterns
3. **Add proper authentication** for protected endpoints
4. **Include comprehensive tests** for all endpoints
5. **Document API changes** in this README

### Help

- Check the [Django documentation](https://docs.djangoproject.com/)
- Review [Django REST Framework docs](https://www.django-rest-framework.org/)
