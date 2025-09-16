from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    health, info,
    UserViewSet, ExerciseViewSet, WorkoutViewSet, WorkoutSessionViewSet,
    GoalViewSet, DietPlanViewSet, MealViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'exercises', ExerciseViewSet)
router.register(r'workouts', WorkoutViewSet)
router.register(r'sessions', WorkoutSessionViewSet)
router.register(r'goals', GoalViewSet)
router.register(r'diets', DietPlanViewSet)
router.register(r'meals', MealViewSet)

urlpatterns = [
    path('health/', health, name='health'),
    path('info/', info, name='info'),
    path('', include(router.urls)),
]
