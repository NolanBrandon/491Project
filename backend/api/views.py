from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import (
    User,
    UserMetrics,
    Goal,
    Exercise,
    Muscle,
    ExerciseMuscle,
    Equipment,
    ExerciseEquipment,
    BodyPart,
    ExerciseBodyPart,
    Keyword,
    ExerciseKeyword,
    RelatedExercise,
    WorkoutPlan,
    PlanDay,
    PlanExercise,
    WorkoutLog,
    Food,
    NutritionLog,
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
    ExerciseSerializer,
    MuscleSerializer,
    ExerciseMuscleSerializer,
    EquipmentSerializer,
    ExerciseEquipmentSerializer,
    BodyPartSerializer,
    ExerciseBodyPartSerializer,
    KeywordSerializer,
    ExerciseKeywordSerializer,
    RelatedExerciseSerializer,
    WorkoutPlanSerializer,
    PlanDaySerializer,
    PlanExerciseSerializer,
    WorkoutLogSerializer,
    FoodSerializer,
    NutritionLogSerializer,
    MealPlanSerializer,
    MealPlanDaySerializer,
    RecipeSerializer,
    MealPlanEntrySerializer,
    IngredientSerializer,
    RecipeIngredientSerializer,
    TagSerializer,
    RecipeTagSerializer
)

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

class MuscleViewSet(viewsets.ModelViewSet):
    queryset = Muscle.objects.all()
    serializer_class = MuscleSerializer
    permission_classes = [AllowAny]

class ExerciseMuscleViewSet(viewsets.ModelViewSet):
    queryset = ExerciseMuscle.objects.all()
    serializer_class = ExerciseMuscleSerializer
    permission_classes = [AllowAny]

class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [AllowAny]

class ExerciseEquipmentViewSet(viewsets.ModelViewSet):
    queryset = ExerciseEquipment.objects.all()
    serializer_class = ExerciseEquipmentSerializer
    permission_classes = [AllowAny]

class BodyPartViewSet(viewsets.ModelViewSet):
    queryset = BodyPart.objects.all()
    serializer_class = BodyPartSerializer
    permission_classes = [AllowAny]

class ExerciseBodyPartViewSet(viewsets.ModelViewSet):
    queryset = ExerciseBodyPart.objects.all()
    serializer_class = ExerciseBodyPartSerializer
    permission_classes = [AllowAny]

class KeywordViewSet(viewsets.ModelViewSet):
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer
    permission_classes = [AllowAny]

class ExerciseKeywordViewSet(viewsets.ModelViewSet):
    queryset = ExerciseKeyword.objects.all()
    serializer_class = ExerciseKeywordSerializer
    permission_classes = [AllowAny]

class RelatedExerciseViewSet(viewsets.ModelViewSet):
    queryset = RelatedExercise.objects.all()
    serializer_class = RelatedExerciseSerializer
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

class WorkoutLogViewSet(viewsets.ModelViewSet):
    queryset = WorkoutLog.objects.all()
    serializer_class = WorkoutLogSerializer
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

# -------------------------------
# Health Check & API Info Views
# -------------------------------
@api_view(['GET'])
def health_check(request):
    """Simple health check endpoint."""
    return Response({"status": "healthy"})




@api_view(['GET'])
def api_info(request):
    """Returns basic API info."""
    return Response({
        "name": "EasyFitness API",
        "version": "1.0",
        "endpoints": [
            "/health/",
            "/info/",
            "/users/",
            "/user-metrics/",
            "/goals/",
            "/foods/",
            "/nutrition-logs/",
            "/exercises/",
            "/workout-plans/",
            "/plan-days/",
            "/plan-exercises/",
            "/meal-plans/",
            "/meal-plan-days/",
            "/recipes/",
            "/meal-plan-entries/",
            "/ingredients/",
            "/recipe-ingredients/",
            "/tags/",
            "/recipe-tags/"
        ]  # ✅ added 'endpoints' key to match test
    })
