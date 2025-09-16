from django.urls import path, include
from rest_framework import routers
from .views import (
    UserViewSet, ExerciseViewSet, WorkoutViewSet, WorkoutSessionViewSet,
    GoalViewSet, DietPlanViewSet, MealViewSet, health, info
)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'exercises', ExerciseViewSet)
router.register(r'workouts', WorkoutViewSet)
router.register(r'sessions', WorkoutSessionViewSet)
router.register(r'goals', GoalViewSet)
router.register(r'diets', DietPlanViewSet)
router.register(r'meals', MealViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('health/', health),
    path('info/', info),
]
