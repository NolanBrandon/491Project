from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    UserMetricViewSet,
    GoalViewSet,
    NutritionLogViewSet,
    WorkoutPlanViewSet,
    WorkoutLogViewSet,
    MealPlanViewSet,
    health_check,
    api_info,
    generate_enriched_workout_plan,
    generate_enriched_meal_plan,
    test_ai_services
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'user-metrics', UserMetricViewSet)
router.register(r'goals', GoalViewSet)
router.register(r'nutrition-logs', NutritionLogViewSet)
router.register(r'workout-plans', WorkoutPlanViewSet)
router.register(r'workout-logs', WorkoutLogViewSet)
router.register(r'meal-plans', MealPlanViewSet)

urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('info/', api_info, name='api_info'),
    path('generate-workout-plan/', generate_enriched_workout_plan, name='generate_enriched_workout_plan'),
    path('generate-meal-plan/', generate_enriched_meal_plan, name='generate_enriched_meal_plan'),
    path('test-ai-services/', test_ai_services, name='test_ai_services'),
    path('', include(router.urls)),
]
