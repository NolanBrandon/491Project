from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import UserProfile, Exercise, Workout, WorkoutSession, Goal, DietPlan, Meal
from .serializers import UserProfileSerializer, ExerciseSerializer, WorkoutSerializer, WorkoutSessionSerializer, GoalSerializer, DietPlanSerializer, MealSerializer

@api_view(['GET'])
def health(request):
    return Response({"status": "healthy", "message": "EasyFitness API is running successfully!", "version": "1.0.0"})

@api_view(['GET'])
def info(request):
    return Response({
        "name": "EasyFitness API",
        "version": "1.0.0",
        "description": "Backend API for the EasyFitness application",
        "endpoints": {
            "health": "/api/health/",
            "info": "/api/info/",
            "users": "/api/users/",
            "profiles": "/api/profiles/",
            "workouts": "/api/workouts/",
            "sessions": "/api/sessions/",
            "goals": "/api/goals/",
            "diets": "/api/diets/"
        }
    })

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer

class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

class WorkoutViewSet(viewsets.ModelViewSet):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer

class WorkoutSessionViewSet(viewsets.ModelViewSet):
    queryset = WorkoutSession.objects.all()
    serializer_class = WorkoutSessionSerializer

class GoalViewSet(viewsets.ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer

class DietPlanViewSet(viewsets.ModelViewSet):
    queryset = DietPlan.objects.all()
    serializer_class = DietPlanSerializer

class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
