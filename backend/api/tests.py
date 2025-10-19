from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import (
    User,
    UserMetrics,
    Goal,
    NutritionLog,
    WorkoutPlan,
    MealPlan,
)
from .serializers import (
    UserSerializer,
    UserMetricsSerializer,
    GoalSerializer,
    NutritionLogSerializer,
    WorkoutPlanSerializer,
    MealPlanSerializer,
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
class NutritionLogViewSet(viewsets.ModelViewSet):
    queryset = NutritionLog.objects.all()
    serializer_class = NutritionLogSerializer
    permission_classes = [AllowAny]

# -------------------------------
# Workout Views
# -------------------------------
class WorkoutPlanViewSet(viewsets.ModelViewSet):
    queryset = WorkoutPlan.objects.all()
    serializer_class = WorkoutPlanSerializer
    permission_classes = [AllowAny]

# -------------------------------
# Meal Plan Views
# -------------------------------
class MealPlanViewSet(viewsets.ModelViewSet):
    queryset = MealPlan.objects.all()
    serializer_class = MealPlanSerializer
    permission_classes = [AllowAny]

# -------------------------------
# Health Check & API Info Views
# -------------------------------
@api_view(['GET'])
def health_check(request):
    """Simple health check endpoint."""
    return Response({
        "status": "healthy",
        "message": "API is up",
        "version": "1.0"
    })

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
            "/nutrition-logs/",
            "/workout-plans/",
            "/meal-plans/"
        ]
    })
