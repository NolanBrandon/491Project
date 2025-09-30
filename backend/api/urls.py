from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    UserMetricViewSet,
    GoalViewSet,
    FoodViewSet,
    NutritionLogViewSet,
    ExerciseViewSet,
    WorkoutPlanViewSet,
    PlanDayViewSet,
    PlanExerciseViewSet,
    MealPlanViewSet,
    MealPlanDayViewSet,
    RecipeViewSet,
    MealPlanEntryViewSet,
    IngredientViewSet,
    RecipeIngredientViewSet,
    TagViewSet,
    RecipeTagViewSet,
    health_check,
    api_info
)

# Create a router and register all viewsets
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'user-metrics', UserMetricViewSet)
router.register(r'goals', GoalViewSet)
router.register(r'foods', FoodViewSet)
router.register(r'nutrition-logs', NutritionLogViewSet)
router.register(r'exercises', ExerciseViewSet)
router.register(r'workout-plans', WorkoutPlanViewSet)
router.register(r'plan-days', PlanDayViewSet)
router.register(r'plan-exercises', PlanExerciseViewSet)
router.register(r'meal-plans', MealPlanViewSet)
router.register(r'meal-plan-days', MealPlanDayViewSet)
router.register(r'recipes', RecipeViewSet)
router.register(r'meal-plan-entries', MealPlanEntryViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'recipe-ingredients', RecipeIngredientViewSet)
router.register(r'tags', TagViewSet)
router.register(r'recipe-tags', RecipeTagViewSet)

# URL patterns
urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('info/', api_info, name='api_info'),
    path('', include(router.urls)),
]
