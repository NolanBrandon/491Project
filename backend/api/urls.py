from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views  # import the views file

# DRF router for all ViewSets
router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'user-metrics', views.UserMetricViewSet)
router.register(r'goals', views.GoalViewSet)
router.register(r'foods', views.FoodViewSet)
router.register(r'nutrition-logs', views.NutritionLogViewSet)
router.register(r'exercises', views.ExerciseViewSet)
router.register(r'workout-plans', views.WorkoutPlanViewSet)
router.register(r'plan-days', views.PlanDayViewSet)
router.register(r'plan-exercises', views.PlanExerciseViewSet)
router.register(r'meal-plans', views.MealPlanViewSet)
router.register(r'meal-plan-days', views.MealPlanDayViewSet)
router.register(r'recipes', views.RecipeViewSet)
router.register(r'meal-plan-entries', views.MealPlanEntryViewSet)
router.register(r'ingredients', views.IngredientViewSet)
router.register(r'recipe-ingredients', views.RecipeIngredientViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'recipe-tags', views.RecipeTagViewSet)

# Include both the router URLs and the health/info endpoints
urlpatterns = [
    path('', include(router.urls)),
    path('health/', views.health_check, name='health_check'),  # ✅ add health check
    path('info/', views.api_info, name='api_info'),            # ✅ add API info
]
