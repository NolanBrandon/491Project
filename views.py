from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User, UserProfile, UserMetrics, Goals
from .serializers import (UserRegistrationSerializer, UserSerializer, UserProfileSerializer, UserMetricsSerializer, GoalsSerializer)

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    try:
        connection.ensure_connection()
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return Response({
        'status': 'ok',
        'database': db_status,
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def api_info(request):
    return Response({
        'name': 'Fitness Tracker API',
        'version': '1.0.0',
        'endpoints': {
            'health': '/api/health/',
            'info': '/api/info/',
            'auth': {
                'register': '/api/auth/register/',
                'login': '/api/auth/login/',
                'refresh': '/api/auth/token/refresh/',
                'me': '/api/auth/me/',
            },
            'profile': '/api/profile/',
            'metrics': '/api/metrics/',
            'goals': '/api/goals/',
        }
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response(
            {'error': 'Email and password are required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(request, username=email, password=password)
    
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    
    return Response(
        {'error': 'Invalid credentials'}, 
        status=status.HTTP_401_UNAUTHORIZED
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)



class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile


class UserMetricsListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserMetricsSerializer

    def get_queryset(self):
        return UserMetrics.objects.filter(user=self.request.user).order_by('-id')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserMetricsDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserMetricsSerializer

    def get_queryset(self):
        return UserMetrics.objects.filter(user=self.request.user)

class GoalsListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GoalsSerializer

    def get_queryset(self):
        return Goals.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GoalsDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GoalsSerializer

    def get_queryset(self):
        return Goals.objects.filter(user=self.request.user)
