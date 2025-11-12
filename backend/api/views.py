from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.response import Response
from .permissions import IsAuthenticatedWithSession, IsOwnerOrReadOnly
import logging

logger = logging.getLogger(__name__)
from .models import (
    User,
    UserMetrics,
    Goal,
    WorkoutPlan,
    WorkoutLog,
    NutritionLog,
    MealPlan,
)
from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserProfileSerializer,
    LoginSerializer,
    ChangePasswordSerializer,
    ChangeUsernameSerializer,
    ChangeEmailSerializer,
    DeleteAccountSerializer,
    UserMetricsSerializer,
    UserMetricsCreateSerializer,
    GoalSerializer,
    GoalCreateSerializer,
    WorkoutPlanSerializer,
    WorkoutPlanDetailSerializer,
    WorkoutLogSerializer,
    NutritionLogSerializer,
    MealPlanSerializer,
    MealPlanDetailSerializer,
)

# -------------------------------
# User & Metrics Views
# -------------------------------
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer  # Default to profile serializer (no password)
    permission_classes = [AllowAny]  # Default, overridden by get_permissions
    
    def get_permissions(self):
        """
        Set permissions based on action.
        - create, login, logout, session, validate_session: AllowAny
        - all other actions: IsAuthenticatedWithSession
        """
        if self.action in ['create', 'login', 'logout', 'session', 'validate_session']:
            return [AllowAny()]
        return [IsAuthenticatedWithSession(), IsOwnerOrReadOnly()]
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserSerializer
        return UserProfileSerializer
    
    def create(self, request, *args, **kwargs):
        """Create user with password hashing and auto-login"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Auto-login: Create session for newly registered user
        request.session['user_id'] = str(user.id)
        request.session['username'] = user.username
        request.session.save()
        
        # Return profile data (without password)
        profile_serializer = UserProfileSerializer(user)
        return Response({
            'message': 'User created and logged in successfully',
            'user': profile_serializer.data
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        """Login endpoint with session management"""
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
                # Create session
                request.session['user_id'] = str(user.id)
                request.session['username'] = user.username
                request.session.save()
                
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
    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        """Logout endpoint - clears session and cookie"""
        if request.session.get('user_id'):
            request.session.flush()  # Clear all session data
            response = Response({'message': 'Logout successful'})
            # Delete the session cookie
            response.delete_cookie(
                'easyfitness_session',
                path='/',
                domain=None,
                samesite='Lax'
            )
            # Also delete CSRF cookie
            response.delete_cookie(
                'easyfitness_csrf',
                path='/',
                domain=None
            )
            return response
        return Response(
            {'error': 'No active session'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=False, methods=['get'])
    def session(self, request):
        """Get current session user"""
        user_id = request.session.get('user_id')
        if not user_id:
            return Response(
                {'error': 'Not authenticated'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        try:
            user = User.objects.get(id=user_id)
            user_data = UserProfileSerializer(user).data
            return Response({
                'authenticated': True,
                'user': user_data
            })
        except User.DoesNotExist:
            # Session has invalid user, clear it
            request.session.flush()
            return Response(
                {'error': 'Invalid session'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
    
    @action(detail=False, methods=['get'])
    def validate_session(self, request):
        """Quick session validation without returning user data"""
        user_id = request.session.get('user_id')
        if user_id:
            try:
                User.objects.get(id=user_id)
                return Response({'valid': True, 'user_id': user_id})
            except User.DoesNotExist:
                request.session.flush()
                return Response({'valid': False}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'valid': False}, status=status.HTTP_401_UNAUTHORIZED)
    
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

    @action(detail=True, methods=['post'])
    def change_username(self, request, pk=None):
        """Change user username with password confirmation"""
        user = self.get_object()
        serializer = ChangeUsernameSerializer(
            data=request.data,
            context={'user': user}
        )

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        new_username = serializer.validated_data['new_username']

        # Update username
        user.username = new_username
        user.save()

        # Update session username
        request.session['username'] = new_username
        request.session.save()

        return Response({
            'message': 'Username changed successfully',
            'username': new_username
        })

    @action(detail=True, methods=['post'])
    def change_email(self, request, pk=None):
        """Change user email with password confirmation"""
        user = self.get_object()
        serializer = ChangeEmailSerializer(
            data=request.data,
            context={'user': user}
        )

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        new_email = serializer.validated_data['new_email']

        # Update email
        user.email = new_email
        user.save()

        return Response({
            'message': 'Email changed successfully',
            'email': new_email
        })

    def destroy(self, request, *args, **kwargs):
        """Delete user account with password confirmation"""
        user = self.get_object()

        # Validate deletion request with password
        serializer = DeleteAccountSerializer(
            data=request.data,
            context={'user': user}
        )

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Clear session before deletion
        request.session.flush()

        # Delete user (cascades to all related records)
        user.delete()

        # Clear cookies
        response = Response({
            'message': 'Account deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)

        response.delete_cookie(
            'easyfitness_session',
            path='/',
            domain=None,
            samesite='Lax'
        )
        response.delete_cookie(
            'easyfitness_csrf',
            path='/',
            domain=None
        )

        return response

    @action(detail=True, methods=['get'])
    def dashboard(self, request, pk=None):
        """Get user dashboard with workout plans, meal plans, and recent activity.
        Users can only access their own dashboard."""
        user = self.get_object()
        
        # Verify user can only access their own dashboard
        session_user_id = request.session.get('user_id')
        if str(user.id) != session_user_id:
            return Response(
                {"error": "You can only access your own dashboard"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
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

class UserMetricViewSet(viewsets.ModelViewSet):
    queryset = UserMetrics.objects.all()
    serializer_class = UserMetricsSerializer
    permission_classes = [IsAuthenticatedWithSession]

    def get_serializer_class(self):
        """Use UserMetricsCreateSerializer for creation to avoid requiring user field"""
        if self.action == 'create':
            return UserMetricsCreateSerializer
        return UserMetricsSerializer

    def get_queryset(self):
        """Filter metrics to only show user's own data"""
        user_id = self.request.session.get('user_id')
        if user_id:
            return UserMetrics.objects.filter(user__id=user_id)
        return UserMetrics.objects.none()

    def create(self, request, *args, **kwargs):
        """Override create to log validation errors"""
        logger.info(f"Creating user metrics with data: {request.data}")
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            logger.error(f"Validation error: {e}")
            logger.error(f"Serializer errors: {serializer.errors}")
            raise
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        """Auto-assign the authenticated user to the metrics"""
        user_id = self.request.session.get('user_id')
        user = User.objects.get(id=user_id)
        serializer.save(user=user)

class GoalViewSet(viewsets.ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticatedWithSession]
    
    def get_serializer_class(self):
        """Use GoalCreateSerializer for creation to avoid requiring user field"""
        if self.action == 'create':
            return GoalCreateSerializer
        return GoalSerializer
    
    def get_queryset(self):
        """Filter goals to only show user's own data"""
        user_id = self.request.session.get('user_id')
        if user_id:
            return Goal.objects.filter(user__id=user_id)
        return Goal.objects.none()
    
    def perform_create(self, serializer):
        """Auto-assign the authenticated user to the goal"""
        user_id = self.request.session.get('user_id')
        user = User.objects.get(id=user_id)
        serializer.save(user=user)
    
    def create(self, request, *args, **kwargs):
        """Override create to return full goal data after creation"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # Return the full goal data using GoalSerializer
        goal = Goal.objects.get(id=serializer.instance.id)
        output_serializer = GoalSerializer(goal)
        headers = self.get_success_headers(output_serializer.data)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

# -------------------------------
# Nutrition Views
# -------------------------------
class NutritionLogViewSet(viewsets.ModelViewSet):
    queryset = NutritionLog.objects.all()
    serializer_class = NutritionLogSerializer
    permission_classes = [IsAuthenticatedWithSession]
    
    def get_queryset(self):
        """Filter nutrition logs to only show user's own data"""
        user_id = self.request.session.get('user_id')
        if user_id:
            return NutritionLog.objects.filter(user__id=user_id)
        return NutritionLog.objects.none()

# -------------------------------
# Exercise & Workout Views
# -------------------------------

class WorkoutPlanViewSet(viewsets.ModelViewSet):
    queryset = WorkoutPlan.objects.all()
    serializer_class = WorkoutPlanSerializer
    permission_classes = [IsAuthenticatedWithSession]
    
    def get_queryset(self):
        """Filter workout plans to only show user's own data"""
        user_id = self.request.session.get('user_id')
        if user_id:
            return WorkoutPlan.objects.filter(user__id=user_id)
        return WorkoutPlan.objects.none()
    
    @action(detail=False, methods=['get'], url_path='user/(?P<user_id>[^/.]+)')
    def user_workout_plans(self, request, user_id=None):
        """Get all workout plans for a specific user. Users can only access their own plans."""
        session_user_id = request.session.get('user_id')
        
        # Verify user can only access their own workout plans
        if user_id != session_user_id:
            return Response(
                {"error": "You can only access your own workout plans"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
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
        """Get workout plan with all its workout data from JSON field."""
        try:
            workout_plan = self.get_object()
            serializer = WorkoutPlanDetailSerializer(workout_plan)
            return Response(serializer.data)
        except WorkoutPlan.DoesNotExist:
            return Response(
                {"error": "Workout plan not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )


class WorkoutLogViewSet(viewsets.ModelViewSet):
    queryset = WorkoutLog.objects.all()
    serializer_class = WorkoutLogSerializer
    permission_classes = [IsAuthenticatedWithSession]
    
    def get_queryset(self):
        """Filter workout logs to only show user's own data"""
        user_id = self.request.session.get('user_id')
        if user_id:
            return WorkoutLog.objects.filter(user__id=user_id)
        return WorkoutLog.objects.none()

# -------------------------------
# Meal Plan & Recipe Views
# -------------------------------
class MealPlanViewSet(viewsets.ModelViewSet):
    queryset = MealPlan.objects.all()
    serializer_class = MealPlanSerializer
    permission_classes = [IsAuthenticatedWithSession]
    
    def get_queryset(self):
        """Filter meal plans to only show user's own data"""
        user_id = self.request.session.get('user_id')
        if user_id:
            return MealPlan.objects.filter(user__id=user_id)
        return MealPlan.objects.none()
    
    @action(detail=False, methods=['get'], url_path='user/(?P<user_id>[^/.]+)')
    def user_meal_plans(self, request, user_id=None):
        """Get all meal plans for a specific user. Users can only access their own plans."""
        session_user_id = request.session.get('user_id')
        
        # Verify user can only access their own meal plans
        if user_id != session_user_id:
            return Response(
                {"error": "You can only access your own meal plans"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
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
            "/users/login/",
            "/users/logout/",
            "/users/session/",
            "/users/validate-session/",
            "/users/{id}/dashboard/",
            "/user-metrics/",
            "/goals/",
            "/workout-plans/",
            "/workout-plans/user/{user_id}/",
            "/workout-logs/",
            "/nutrition-logs/",
            "/meal-plans/",
            "/meal-plans/user/{user_id}/",
            "/generate-meal-plan/",
            "/generate-workout-plan/"
        ]
    })


# ===========================
# AI-Powered Workout Plan Generation
# ===========================

@api_view(['POST'])
@permission_classes([IsAuthenticatedWithSession])
def generate_enriched_workout_plan(request):
    """
    Generate an AI-powered workout plan enriched with ExerciseDB data.
    Requires authentication. Users can only generate plans for themselves.
    
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
        
        # Verify user can only generate plans for themselves
        session_user_id = request.session.get('user_id')
        if user_id != session_user_id:
            return Response({
                'error': 'You can only generate workout plans for yourself'
            }, status=status.HTTP_403_FORBIDDEN)
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
            description=plan_data.get('plan_description', 'Generated by AI'),
            workout_plan_data=plan_data  # Store entire workout plan as JSON
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
@permission_classes([IsAuthenticatedWithSession])
def generate_enriched_meal_plan(request):
    """
    Generate AI-powered meal plan with nutritional data and save to database.
    Requires authentication. Users can only generate plans for themselves.
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
        
        # Verify user can only generate plans for themselves
        session_user_id = request.session.get('user_id')
        if user_id != session_user_id:
            return Response({
                'success': False,
                'error': 'You can only generate meal plans for yourself'
            }, status=status.HTTP_403_FORBIDDEN)
        
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
        
        logger.info(f"🍽️ Starting meal plan generation for user {user_id}")
        logger.info(f"📊 Parameters: {daily_calorie_target} calories, {days_count} days, preferences: {dietary_preferences}")
        logger.info(f"👤 User profile: {user_profile}")
        
        # Generate AI meal plan with detailed logging
        logger.info("🤖 Calling Gemini AI service for meal plan generation...")
        logger.info("⏱️ This may take 30-60 seconds for complex meal plans...")
        
        try:
            ai_result = ai_service.generate_meal_plan(
                user_goal=goal,
                daily_calorie_target=daily_calorie_target,
                dietary_preferences=dietary_preferences,
                user_profile=user_profile
            )
            logger.info("✅ AI meal plan generation completed")
        except Exception as ai_error:
            logger.error(f"❌ AI meal plan generation failed: {ai_error}")
            return Response({
                'success': False,
                'error': 'AI meal plan generation failed',
                'details': str(ai_error),
                'suggestion': 'Please try again with simpler preferences or contact support if the issue persists'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        if not ai_result.get('success'):
            return Response({
                'success': False,
                'error': 'AI meal plan generation failed',
                'details': ai_result.get('error', 'Unknown error')
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        meal_plan_data = ai_result['data']
        logger.info(f"📝 Generated meal plan: '{meal_plan_data.get('plan_name', 'Unknown Plan')}'")
        logger.info(f"📅 Days generated: {len(meal_plan_data.get('days', []))}")
        
        # Log meal structure
        for i, day in enumerate(meal_plan_data.get('days', [])[:2], 1):  # Log first 2 days
            meals = day.get('meals', {})
            logger.info(f"🗓️ Day {day.get('day_number', i)}: {len(meals)} meals - {list(meals.keys())}")
        
        # Save to database
        logger.info("💾 Saving meal plan to database...")
        try:
            saved_plan_id = _save_meal_plan_to_database(
                user, 
                meal_plan_data, 
                daily_calorie_target, 
                dietary_preferences, 
                goal
            )
            logger.info(f"✅ Meal plan saved successfully with ID: {saved_plan_id}")
        except Exception as db_error:
            logger.error(f"❌ Database save failed: {db_error}")
            return Response({
                'success': False,
                'error': 'Meal plan generated but failed to save to database',
                'details': str(db_error),
                'ai_data': meal_plan_data  # Include the generated data for debugging
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
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


def _save_meal_plan_to_database(user, meal_plan_data, daily_calorie_target, dietary_preferences, goal):
    """
    Save AI-generated meal plan to database with complete nutritional data.
    """
    try:
        # Extract metadata for easy filtering
        days_count = len(meal_plan_data.get('days', []))
        
        # Try to extract calorie target from the plan description if not provided
        if not daily_calorie_target:
            description = meal_plan_data.get('plan_description', '')
            if 'kcal' in description or 'calories' in description:
                import re
                calorie_match = re.search(r'(\d+)\s*(?:kcal|calories)', description)
                if calorie_match:
                    daily_calorie_target = int(calorie_match.group(1))
        
        # Create simplified meal plan with all data stored as JSON
        meal_plan = MealPlan.objects.create(
            user=user,
            name=meal_plan_data.get('plan_name', 'AI Generated Meal Plan'),
            description=meal_plan_data.get('plan_description', 'AI-generated personalized meal plan'),
            meal_plan_data=meal_plan_data,  # Store complete AI response
            daily_calorie_target=daily_calorie_target,
            days_count=days_count,
            dietary_preferences=dietary_preferences or [],
            goal=goal or ''
        )
        
        logger.info(f"Successfully saved meal plan {meal_plan.id} to database")
        return meal_plan.id
        
    except Exception as e:
        logger.error(f"Error saving meal plan to database: {e}")
        raise
