from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    UserMetricViewSet,
    GoalViewSet,
    FoodViewSet,
    NutritionLogViewSet,
    ExerciseViewSet,
    MuscleViewSet,
    ExerciseMuscleViewSet,
    EquipmentViewSet,
    ExerciseEquipmentViewSet,
    BodyPartViewSet,
    ExerciseBodyPartViewSet,
    KeywordViewSet,
    ExerciseKeywordViewSet,
    RelatedExerciseViewSet,
    WorkoutPlanViewSet,
    PlanDayViewSet,
    PlanExerciseViewSet,
    WorkoutLogViewSet,
    MealPlanViewSet,
    MealPlanDayViewSet,
    RecipeViewSet,
    MealPlanEntryViewSet,
    IngredientViewSet,
    RecipeIngredientViewSet,
    TagViewSet,
    RecipeTagViewSet,
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
router.register(r'foods', FoodViewSet)
router.register(r'nutrition-logs', NutritionLogViewSet)
router.register(r'exercises', ExerciseViewSet)
router.register(r'muscles', MuscleViewSet)
router.register(r'exercise-muscles', ExerciseMuscleViewSet)
router.register(r'equipment', EquipmentViewSet)
router.register(r'exercise-equipment', ExerciseEquipmentViewSet)
router.register(r'body-parts', BodyPartViewSet)
router.register(r'exercise-body-parts', ExerciseBodyPartViewSet)
router.register(r'keywords', KeywordViewSet)
router.register(r'exercise-keywords', ExerciseKeywordViewSet)
router.register(r'related-exercises', RelatedExerciseViewSet)
router.register(r'workout-plans', WorkoutPlanViewSet)
router.register(r'plan-days', PlanDayViewSet)
router.register(r'plan-exercises', PlanExerciseViewSet)
router.register(r'workout-logs', WorkoutLogViewSet)
router.register(r'meal-plans', MealPlanViewSet)
router.register(r'meal-plan-days', MealPlanDayViewSet)
router.register(r'recipes', RecipeViewSet)
router.register(r'meal-plan-entries', MealPlanEntryViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'recipe-ingredients', RecipeIngredientViewSet)
router.register(r'tags', TagViewSet)
router.register(r'recipe-tags', RecipeTagViewSet)

urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('info/', api_info, name='api_info'),
    path('generate-workout-plan/', generate_enriched_workout_plan, name='generate_enriched_workout_plan'),
    path('generate-meal-plan/', generate_enriched_meal_plan, name='generate_enriched_meal_plan'),
    path('test-ai-services/', test_ai_services, name='test_ai_services'),
    path('', include(router.urls)),
]
