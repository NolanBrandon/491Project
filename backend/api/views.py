from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import (
    User,
    UserMetrics,
    Goal,
    Food,
    NutritionLog,
    Exercise,
    WorkoutPlan,
    PlanDay,
    PlanExercise,
    MealPlan,
    MealPlanDay,
    Recipe,
    MealPlanEntry,
    Ingredient,
    RecipeIngredient,
    Tag,
    RecipeTag
)
from .serializers import (
    UserSerializer,
    UserMetricsSerializer,
    GoalSerializer,
    FoodSerializer,
    NutritionLogSerializer,
    ExerciseSerializer,
    WorkoutPlanSerializer,
    PlanDaySerializer,
    PlanExerciseSerializer,
    MealPlanSerializer,
    MealPlanDaySerializer,
    RecipeSerializer,
    MealPlanEntrySerializer,
    IngredientsSerializer,
    RecipeIngredientSerializer,
    TagSerializer,
    RecipeTagSerializer
)

# -------------------------------
# Health Check & API Info Views
# -------------------------------
@api_view(['GET'])
def health_check(request):
    """
    Health check endpoint compatible with automated tests.
    Returns 'status', 'message', and 'version'.
    """
    return Response({
        'status': 'healthy',
        'message': 'healthy',
        'version': '1.0.0'
    })


@api_view(['GET'])
def api_info(request):
    """
    API info endpoint.
    Returns basic info and endpoints key for test compatibility.
    """
    return Response({
        'name': 'EasyFitness API',
        'version': '1.0.0',
        'endpoints': [
            '/api/users/',
            '/api/user-metrics/',
            '/api/goals/',
            '/api/foods/',
            '/api/nutrition-logs/',
            '/api/exercises/',
            '/api/workout-plans/',
            '/api/plan-days/',
            '/api/plan-exercises/',
            '/api/meal-plans/',
            '/api/meal-plan-days/',
            '/api/recipes/',
            '/api/meal-plan-entries/',
            '/api/ingredients/',
            '/api/recipe-ingredients/',
            '/api/tags/',
            '/api/recipe-tags/'
        ]
    })



# -------------------------------
# User & Metrics Views
# -------------------------------
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class UserMetricViewSet(viewsets.ModelViewSet):
    queryset = UserMetrics.objects.all()
    serializer_class = UserMetricsSerializer
    permission_classes = [AllowAny]

class GoalViewSet(viewsets.ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    permission_classes = [AllowAny]


# -------------------------------
# Nutrition Views
# -------------------------------
class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [AllowAny]

class NutritionLogViewSet(viewsets.ModelViewSet):
    queryset = NutritionLog.objects.all()
    serializer_class = NutritionLogSerializer
    permission_classes = [AllowAny]


# -------------------------------
# Exercise & Workout Views
# -------------------------------
class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [AllowAny]

class WorkoutPlanViewSet(viewsets.ModelViewSet):
    queryset = WorkoutPlan.objects.all()
    serializer_class = WorkoutPlanSerializer
    permission_classes = [AllowAny]

class PlanDayViewSet(viewsets.ModelViewSet):
    queryset = PlanDay.objects.all()
    serializer_class = PlanDaySerializer
    permission_classes = [AllowAny]

class PlanExerciseViewSet(viewsets.ModelViewSet):
    queryset = PlanExercise.objects.all()
    serializer_class = PlanExerciseSerializer
    permission_classes = [AllowAny]


# -------------------------------
# Meal Plan & Recipe Views
# -------------------------------
class MealPlanViewSet(viewsets.ModelViewSet):
    queryset = MealPlan.objects.all()
    serializer_class = MealPlanSerializer
    permission_classes = [AllowAny]

class MealPlanDayViewSet(viewsets.ModelViewSet):
    queryset = MealPlanDay.objects.all()
    serializer_class = MealPlanDaySerializer
    permission_classes = [AllowAny]

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [AllowAny]

class MealPlanEntryViewSet(viewsets.ModelViewSet):
    queryset = MealPlanEntry.objects.all()
    serializer_class = MealPlanEntrySerializer
    permission_classes = [AllowAny]

class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = [AllowAny]

class RecipeIngredientViewSet(viewsets.ModelViewSet):
    queryset = RecipeIngredient.objects.all()
    serializer_class = RecipeIngredientSerializer
    permission_classes = [AllowAny]

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]

class RecipeTagViewSet(viewsets.ModelViewSet):
    queryset = RecipeTag.objects.all()
    serializer_class = RecipeTagSerializer
    permission_classes = [AllowAny]
