from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)
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
    UserCreateSerializer,
    UserProfileSerializer,
    LoginSerializer,
    ChangePasswordSerializer,
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
    MealPlanDetailSerializer,
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
    serializer_class = UserProfileSerializer  # Default to profile serializer (no password)
    permission_classes = [AllowAny]
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserSerializer
        return UserProfileSerializer
    
    def create(self, request, *args, **kwargs):
        """Create user with password hashing"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Return profile data (without password)
        profile_serializer = UserProfileSerializer(user)
        return Response(profile_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        """Simple login endpoint"""
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        try:
            user = User.objects.get(username=username)
            # Import the verification function
            from .serializers import verify_password
            if verify_password(password, user.password_hash):
                user_data = UserProfileSerializer(user).data
                return Response({
                    'message': 'Login successful',
                    'user': user_data
                })
            else:
                return Response(
                    {'error': 'Invalid credentials'}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except User.DoesNotExist:
            return Response(
                {'error': 'Invalid credentials'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
    
    @action(detail=True, methods=['post'])
    def change_password(self, request, pk=None):
        """Change user password"""
        user = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']
        
        from .serializers import verify_password, hash_password
        if verify_password(old_password, user.password_hash):
            user.password_hash = hash_password(new_password)
            user.save()
            return Response({'message': 'Password changed successfully'})
        else:
            return Response(
                {'error': 'Invalid old password'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
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
        """Get meal plan with all its days, entries, recipes, and ingredients."""
        try:
            meal_plan = self.get_object()
            serializer = MealPlanDetailSerializer(meal_plan)
            return Response(serializer.data)
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


# ===========================
# AI-Powered Workout Plan Generation
# ===========================

@api_view(['POST'])
def generate_enriched_workout_plan(request):
    """
    Generate an AI-powered workout plan enriched with ExerciseDB data.
    
    Expected request body:
    {
        "user_id": "uuid",
        "user_goal": "build muscle",
        "experience_level": "beginner",
        "days_per_week": 4,
        "save_plan": true  // optional, defaults to false
    }
    """
    try:
        # Validate request data
        user_id = request.data.get('user_id')
        user_goal = request.data.get('user_goal')
        experience_level = request.data.get('experience_level')
        days_per_week = request.data.get('days_per_week')
        save_plan = request.data.get('save_plan', False)
        
        if not all([user_id, user_goal, experience_level, days_per_week]):
            return Response({
                'error': 'Missing required fields: user_id, user_goal, experience_level, days_per_week'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate user exists
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({
                'error': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Prepare user profile for AI
        user_profile = {
            'age': user.get_age() if hasattr(user, 'get_age') else None,
            'gender': user.gender,
            'username': user.username
        }
        
        # Initialize AI service
        from api.services.ai_service import GeminiAIService
        ai_service = GeminiAIService()
        
        # Generate AI workout plan
        ai_result = ai_service.generate_exercise_plan(
            user_goal=user_goal,
            experience_level=experience_level,
            days_per_week=days_per_week,
            user_profile=user_profile
        )
        
        if not ai_result.get('success', False):
            return Response({
                'error': 'Failed to generate AI workout plan',
                'details': ai_result.get('error', 'Unknown error')
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Initialize Exercise service for enrichment
        from api.services.exercise_service import ExerciseDBService
        exercise_service = ExerciseDBService()
        
        # Enrich the AI plan with ExerciseDB data
        enriched_result = exercise_service.enrich_workout_plan(ai_result)
        
        if not enriched_result.get('success', False):
            # Return AI plan even if enrichment fails
            return Response({
                'success': True,
                'data': ai_result['data'],
                'enrichment_failed': True,
                'enrichment_error': enriched_result.get('error', 'Unknown enrichment error'),
                'message': 'Workout plan generated but enrichment failed'
            }, status=status.HTTP_200_OK)
        
        # Optionally save the plan to database
        saved_plan_id = None
        if save_plan:
            try:
                saved_plan_id = save_workout_plan_to_database(user, enriched_result['data'])
            except Exception as e:
                logger.error(f"Failed to save workout plan: {e}")
                # Continue without saving, don't fail the entire request
        
        response_data = {
            'success': True,
            'data': enriched_result['data'],
            'enrichment_stats': enriched_result.get('enrichment_stats', {}),
            'message': 'Enriched workout plan generated successfully',
            'user_id': user_id,
            'generation_params': {
                'user_goal': user_goal,
                'experience_level': experience_level,
                'days_per_week': days_per_week
            }
        }
        
        if saved_plan_id:
            response_data['saved_plan_id'] = saved_plan_id
            response_data['message'] += ' and saved to database'
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error generating enriched workout plan: {e}")
        return Response({
            'error': 'Internal server error',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def save_workout_plan_to_database(user, plan_data):
    """
    Save an enriched workout plan to the database.
    
    Args:
        user: User instance
        plan_data: Enriched workout plan data
        
    Returns:
        str: ID of the saved workout plan
    """
    try:
        # Create the main workout plan
        workout_plan = WorkoutPlan.objects.create(
            user=user,
            name=plan_data.get('plan_name', 'AI Generated Plan'),
            description=plan_data.get('plan_description', 'Generated by AI')
        )
        
        # Create plan days and exercises
        for day_data in plan_data.get('days', []):
            plan_day = PlanDay.objects.create(
                plan=workout_plan,
                day_number=day_data.get('day_number', 1),
                name=day_data.get('day_name', f"Day {day_data.get('day_number', 1)}")
            )
            
            # Create exercises for this day
            for exercise_data in day_data.get('exercises', []):
                # Try to find existing exercise or create new one
                exercise_name = exercise_data.get('exercise_name', '')
                exercise_details = exercise_data.get('exercise_details')
                
                # Look for existing exercise by name first
                exercise = None
                if exercise_details and exercise_details.get('exerciseId'):
                    # Try to find by ExerciseDB ID first
                    try:
                        exercise = Exercise.objects.get(exerciseDbId=exercise_details['exerciseId'])
                    except Exercise.DoesNotExist:
                        pass
                
                if not exercise:
                    # Create new exercise
                    exercise_db_id = exercise_details.get('exerciseId') if exercise_details else ''
                    exercise = Exercise.objects.create(
                        name=exercise_name,
                        exerciseDbId=exercise_db_id or '',  # Use empty string if None
                        image_url=exercise_details.get('imageUrl') if exercise_details else None,
                        video_url=exercise_details.get('videoUrl') if exercise_details else None,
                        overview=exercise_details.get('overview') if exercise_details else None,
                        instructions=exercise_details.get('instructions', []) if exercise_details else [],
                        exercise_type=exercise_details.get('exerciseType') if exercise_details else None
                    )
                
                # Create plan exercise
                PlanExercise.objects.create(
                    plan_day=plan_day,
                    exercise=exercise,
                    display_order=len(day_data.get('exercises', [])),
                    sets=exercise_data.get('sets', 1),
                    reps=str(exercise_data.get('reps', '10')),
                    rest_period_seconds=exercise_data.get('rest_period_seconds')
                )
        
        logger.info(f"Successfully saved workout plan '{workout_plan.name}' for user {user.username}")
        return str(workout_plan.id)
        
    except Exception as e:
        logger.error(f"Error saving workout plan to database: {e}")
        raise


@api_view(['GET'])
def test_ai_services(request):
    """
    Test endpoint to verify AI and Exercise services are working.
    """
    try:
        # Test AI service
        from api.services.ai_service import GeminiAIService
        ai_service = GeminiAIService()
        ai_test_success, ai_test_message = ai_service.test_connection()
        
        # Test Exercise service
        from api.services.exercise_service import ExerciseDBService
        exercise_service = ExerciseDBService()
        exercise_test_success, exercise_test_message = exercise_service.test_connection()
        
        return Response({
            'ai_service': {
                'status': 'working' if ai_test_success else 'failed',
                'message': ai_test_message
            },
            'exercise_service': {
                'status': 'working' if exercise_test_success else 'failed',
                'message': exercise_test_message
            },
            'overall_status': 'ready' if (ai_test_success and exercise_test_success) else 'issues_detected'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': 'Failed to test services',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def generate_enriched_meal_plan(request):
    """
    Generate AI-powered meal plan with nutritional data and save to database.
    """
    try:
        # Extract request data
        data = request.data
        user_id = data.get('user_id')
        daily_calorie_target = data.get('daily_calorie_target', 2000)
        dietary_preferences = data.get('dietary_preferences', [])
        goal = data.get('goal', 'maintain weight')
        meal_frequency = data.get('meal_frequency', 3)  # meals per day
        days_count = data.get('days_count', 5)
        gender = data.get('gender', 'other')
        age = data.get('age', 30)
        activity_level = data.get('activity_level', 'moderate')
        
        # Validate required fields
        if not user_id:
            return Response({
                'success': False,
                'error': 'user_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate user exists
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({
                'success': False,
                'error': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Initialize AI service
        from api.services.ai_service import GeminiAIService
        ai_service = GeminiAIService()
        
        # Prepare user profile
        user_profile = {
            'age': age,
            'gender': gender,
            'activity_level': activity_level
        }
        
        logger.info(f"Generating meal plan for user {user_id} with {daily_calorie_target} calories, preferences: {dietary_preferences}")
        
        # Generate AI meal plan
        ai_result = ai_service.generate_meal_plan(
            user_goal=goal,
            daily_calorie_target=daily_calorie_target,
            dietary_preferences=dietary_preferences,
            user_profile=user_profile
        )
        
        if not ai_result.get('success'):
            return Response({
                'success': False,
                'error': 'AI meal plan generation failed',
                'details': ai_result.get('error', 'Unknown error')
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        meal_plan_data = ai_result['data']
        
        # Save to database
        saved_plan_id = _save_meal_plan_to_database(user, meal_plan_data)
        
        return Response({
            'success': True,
            'message': 'AI meal plan generated and saved successfully',
            'saved_plan_id': str(saved_plan_id),
            'plan_name': meal_plan_data.get('plan_name', 'Generated Meal Plan'),
            'total_days': len(meal_plan_data.get('days', [])),
            'daily_calorie_target': daily_calorie_target,
            'ai_generation': {
                'success': True,
                'days_generated': len(meal_plan_data.get('days', [])),
                'meals_per_day': len(meal_plan_data.get('days', [{}])[0].get('meals', {})) if meal_plan_data.get('days') else 0
            }
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        logger.error(f"Error in generate_enriched_meal_plan: {e}")
        return Response({
            'success': False,
            'error': 'Meal plan generation failed',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def _save_meal_plan_to_database(user, meal_plan_data):
    """
    Save AI-generated meal plan to database with recipes and ingredients.
    """
    try:
        # Create main meal plan
        meal_plan = MealPlan.objects.create(
            user=user,
            name=meal_plan_data.get('plan_name', 'AI Generated Meal Plan'),
            description=meal_plan_data.get('plan_description', 'AI-generated personalized meal plan')
        )
        
        # Process each day
        for day_data in meal_plan_data.get('days', []):
            day_number = day_data.get('day_number', 1)
            
            # Create meal plan day
            meal_plan_day = MealPlanDay.objects.create(
                meal_plan=meal_plan,
                day_number=day_number
            )
            
            # Process meals for this day
            meals = day_data.get('meals', {})
            for meal_type, meal_data in meals.items():
                recipe_name = meal_data.get('recipe_name', f'{meal_type.capitalize()} Recipe')
                
                # Create or get recipe
                recipe, created = Recipe.objects.get_or_create(
                    name=recipe_name,
                    defaults={
                        'category': 'AI Generated',
                        'instructions': meal_data.get('instructions', ''),
                        'area': 'Various'
                    }
                )
                
                # Process ingredients for this recipe
                for ingredient_data in meal_data.get('ingredients', []):
                    ingredient_name = ingredient_data.get('ingredient_name', 'Unknown Ingredient')
                    measure = ingredient_data.get('measure', '1 unit')
                    
                    # Create or get ingredient
                    ingredient, created = Ingredient.objects.get_or_create(
                        name=ingredient_name
                    )
                    
                    # Create recipe-ingredient relationship
                    RecipeIngredient.objects.get_or_create(
                        recipe=recipe,
                        ingredient=ingredient,
                        defaults={'measure': measure}
                    )
                
                # Create meal plan entry
                MealPlanEntry.objects.create(
                    meal_plan_day=meal_plan_day,
                    recipe=recipe,
                    meal_type=meal_type
                )
        
        logger.info(f"Successfully saved meal plan {meal_plan.id} to database")
        return meal_plan.id
        
    except Exception as e:
        logger.error(f"Error saving meal plan to database: {e}")
        raise
