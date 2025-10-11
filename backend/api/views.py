from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, action
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
    
    @action(detail=True, methods=['get'])
    def dashboard(self, request, pk=None):
        """Get user dashboard with workout plans, meal plans, and recent activity."""
        try:
            user = self.get_object()
            user_data = UserSerializer(user).data
            
            # Get user's workout plans
            workout_plans = WorkoutPlan.objects.filter(user=user)
            user_data['workout_plans'] = WorkoutPlanSerializer(workout_plans, many=True).data
            
            # Get user's meal plans
            meal_plans = MealPlan.objects.filter(user=user)
            user_data['meal_plans'] = MealPlanSerializer(meal_plans, many=True).data
            
            # Get user's goals
            goals = Goal.objects.filter(user=user, is_active=True)
            user_data['active_goals'] = GoalSerializer(goals, many=True).data
            
            # Get recent workout logs (last 10)
            recent_workouts = WorkoutLog.objects.filter(user=user).order_by('-date_performed')[:10]
            user_data['recent_workouts'] = WorkoutLogSerializer(recent_workouts, many=True).data
            
            # Get latest metrics
            latest_metrics = UserMetrics.objects.filter(user=user).order_by('-date_recorded').first()
            if latest_metrics:
                user_data['latest_metrics'] = UserMetricsSerializer(latest_metrics).data
            
            return Response(user_data)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

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
    
    @action(detail=False, methods=['get'], url_path='user/(?P<user_id>[^/.]+)')
    def user_workout_plans(self, request, user_id=None):
        """Get all workout plans for a specific user."""
        try:
            user = User.objects.get(id=user_id)
            workout_plans = WorkoutPlan.objects.filter(user=user)
            serializer = self.get_serializer(workout_plans, many=True)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['get'])
    def with_details(self, request, pk=None):
        """Get workout plan with all its days and exercises."""
        try:
            workout_plan = self.get_object()
            plan_data = WorkoutPlanSerializer(workout_plan).data
            
            # Get all plan days for this workout plan
            plan_days = PlanDay.objects.filter(plan=workout_plan).order_by('day_number')
            plan_data['days'] = []
            
            for day in plan_days:
                day_data = PlanDaySerializer(day).data
                # Get all exercises for this day
                plan_exercises = PlanExercise.objects.filter(plan_day=day).order_by('display_order')
                day_data['exercises'] = []
                
                for plan_exercise in plan_exercises:
                    exercise_data = PlanExerciseSerializer(plan_exercise).data
                    # Include exercise details
                    exercise_data['exercise_details'] = ExerciseSerializer(plan_exercise.exercise).data
                    day_data['exercises'].append(exercise_data)
                
                plan_data['days'].append(day_data)
            
            return Response(plan_data)
        except WorkoutPlan.DoesNotExist:
            return Response(
                {"error": "Workout plan not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

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
    
    @action(detail=False, methods=['get'], url_path='user/(?P<user_id>[^/.]+)')
    def user_meal_plans(self, request, user_id=None):
        """Get all meal plans for a specific user."""
        try:
            user = User.objects.get(id=user_id)
            meal_plans = MealPlan.objects.filter(user=user)
            serializer = self.get_serializer(meal_plans, many=True)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['get'])
    def with_details(self, request, pk=None):
        """Get meal plan with all its days and entries."""
        try:
            meal_plan = self.get_object()
            plan_data = MealPlanSerializer(meal_plan).data
            
            # Get all meal plan days for this meal plan
            meal_plan_days = MealPlanDay.objects.filter(meal_plan=meal_plan).order_by('day_number')
            plan_data['days'] = []
            
            for day in meal_plan_days:
                day_data = MealPlanDaySerializer(day).data
                # Get all entries for this day
                meal_entries = MealPlanEntry.objects.filter(meal_plan_day=day).order_by('meal_type')
                day_data['entries'] = []
                
                for entry in meal_entries:
                    entry_data = MealPlanEntrySerializer(entry).data
                    # Include food or recipe details
                    if entry.food:
                        entry_data['food_details'] = FoodSerializer(entry.food).data
                    if entry.recipe:
                        entry_data['recipe_details'] = RecipeSerializer(entry.recipe).data
                    day_data['entries'].append(entry_data)
                
                plan_data['days'].append(day_data)
            
            return Response(plan_data)
        except MealPlan.DoesNotExist:
            return Response(
                {"error": "Meal plan not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

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
    serializer_class = IngredientSerializer
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
            "/users/{id}/dashboard/",
            "/user-metrics/",
            "/goals/",
            "/exercises/",
            "/muscles/",
            "/exercise-muscles/",
            "/equipment/",
            "/exercise-equipment/",
            "/body-parts/",
            "/exercise-body-parts/",
            "/keywords/",
            "/exercise-keywords/",
            "/related-exercises/",
            "/workout-plans/",
            "/workout-plans/user/{user_id}/",
            "/workout-plans/{id}/with_details/",
            "/plan-days/",
            "/plan-exercises/",
            "/workout-logs/",
            "/foods/",
            "/nutrition-logs/",
            "/meal-plans/",
            "/meal-plans/user/{user_id}/",
            "/meal-plans/{id}/with_details/",
            "/meal-plan-days/",
            "/recipes/",
            "/meal-plan-entries/",
            "/ingredients/",
            "/recipe-ingredients/",
            "/tags/",
            "/recipe-tags/"
        ]
    })
