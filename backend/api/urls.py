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
    signup,  # 👈 added import
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
    path('signup/', signup, name='signup'),  # 👈 new Supabase signup route
    path('', include(router.urls)),
]
