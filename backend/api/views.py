from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from supabase import create_client, Client

from .models import (
    User,
    UserMetrics,
    Goal,
    NutritionLog,
    WorkoutPlan,
    WorkoutLog,
    MealPlan,
)
from .serializers import (
    UserSerializer,
    UserMetricsSerializer,
    GoalSerializer,
    NutritionLogSerializer,
    WorkoutPlanSerializer,
    WorkoutLogSerializer,
    MealPlanSerializer,
)

# ======================================================
# Health & Info endpoints
# ======================================================
@api_view(['GET'])
def health_check(request):
    return Response({"status": "ok"}, status=status.HTTP_200_OK)


@api_view(['GET'])
def api_info(request):
    return Response({
        "message": "EasyFitness API connected successfully",
        "database": settings.DATABASES["default"]["HOST"],
    }, status=status.HTTP_200_OK)


# ======================================================
# Standard ViewSets for existing models
# ======================================================
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserMetricViewSet(viewsets.ModelViewSet):
    queryset = UserMetrics.objects.all()
    serializer_class = UserMetricsSerializer


class GoalViewSet(viewsets.ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer


class NutritionLogViewSet(viewsets.ModelViewSet):
    queryset = NutritionLog.objects.all()
    serializer_class = NutritionLogSerializer


class WorkoutPlanViewSet(viewsets.ModelViewSet):
    queryset = WorkoutPlan.objects.all()
    serializer_class = WorkoutPlanSerializer


class WorkoutLogViewSet(viewsets.ModelViewSet):
    queryset = WorkoutLog.objects.all()
    serializer_class = WorkoutLogSerializer


class MealPlanViewSet(viewsets.ModelViewSet):
    queryset = MealPlan.objects.all()
    serializer_class = MealPlanSerializer


# ======================================================
# New: Supabase Auth Signup Endpoint (V2 compatible)
# ======================================================
@api_view(['POST'])
def signup(request):
    """
    Handle user signup through Supabase Auth (v2).
    """
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response(
            {"error": "Email and password are required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Initialize Supabase client
    supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

    try:
        result = supabase.auth.sign_up({"email": email, "password": password})

        # Supabase v2 returns a dict instead of a User object sometimes
        if hasattr(result, "user") and result.user is not None:
            return Response(
                {"message": "User created successfully", "user": result.user.email},
                status=status.HTTP_201_CREATED,
            )
        elif isinstance(result, dict) and "user" in result:
            return Response(
                {"message": "User created successfully", "user": result["user"]["email"]},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"error": "Signup failed", "details": str(result)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    except Exception as e:
        return Response(
            {"error": f"Supabase signup failed: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
