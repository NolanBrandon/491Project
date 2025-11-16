from rest_framework import serializers
import hashlib
from django.contrib.auth.hashers import make_password, check_password
from .models import (
    User,
    UserMetrics,
    Goal,
    WorkoutPlan,
    WorkoutPlanCompletionLog,
    WorkoutLog,
    NutritionLog,
    MealPlan,
)

def hash_password(password):
    """
    Hash password using Django's built-in password hashing (PBKDF2 by default).
    This is much more secure than SHA-256 as it:
    - Uses PBKDF2 algorithm with 600,000 iterations (slow by design)
    - Automatically generates and stores salt
    - Is resistant to rainbow table and GPU attacks
    """
    return make_password(password)

def verify_password(password, hashed_password):
    """
    Verify password against hash.
    Supports both:
    - New Django hashes (pbkdf2_sha256$...)
    - Legacy SHA-256 hashes (salt$hash) for backward compatibility
    """
    # Check if it's a Django hash (starts with algorithm identifier)
    if hashed_password.startswith('pbkdf2_') or hashed_password.startswith('argon2') or hashed_password.startswith('bcrypt'):
        return check_password(password, hashed_password)

    # Legacy SHA-256 support (for existing users)
    try:
        salt, hashed = hashed_password.split('$')
        return hashlib.sha256((password + salt).encode()).hexdigest() == hashed
    except ValueError:
        return False

# -------------------------------
# User Serializers
# -------------------------------
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, required=False)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'gender', 'date_of_birth', 'last_login_date', 'login_streak', 'created_at']
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def create(self, validated_data):
        # Hash the password before saving
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.password_hash = hash_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        # Handle password update if provided
        password = validated_data.pop('password', None)
        if password:
            instance.password_hash = hash_password(password)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance

class UserCreateSerializer(serializers.ModelSerializer):
    """Separate serializer for user creation with required password"""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'gender', 'date_of_birth']
        extra_kwargs = {
            'password': {'write_only': True},
            'password_confirm': {'write_only': True},
        }
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')  # Remove confirmation field
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.password_hash = hash_password(password)
        user.save()
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile updates (no password)"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'gender', 'date_of_birth', 'last_login_date', 'login_streak', 'created_at']
        read_only_fields = ['id', 'last_login_date', 'login_streak', 'created_at']

class LoginSerializer(serializers.Serializer):
    """Serializer for login validation"""
    username = serializers.CharField()
    password = serializers.CharField()

class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for password change validation"""
    old_password = serializers.CharField()
    new_password = serializers.CharField(min_length=8)

class ChangeUsernameSerializer(serializers.Serializer):
    """Serializer for username change with password confirmation"""
    new_username = serializers.CharField(min_length=3, max_length=50)
    current_password = serializers.CharField()

    def validate_new_username(self, value):
        """Validate username format (alphanumeric + underscore only)"""
        import re
        if not re.match(r'^[a-zA-Z0-9_]+$', value):
            raise serializers.ValidationError(
                "Username can only contain letters, numbers, and underscores"
            )
        return value

    def validate(self, data):
        """Check if username is already taken"""
        user = self.context.get('user')
        new_username = data['new_username']

        # Check if username is already taken by another user
        if User.objects.filter(username=new_username).exclude(id=user.id).exists():
            raise serializers.ValidationError({
                'new_username': 'This username is already taken'
            })

        # Verify current password
        if not verify_password(data['current_password'], user.password_hash):
            raise serializers.ValidationError({
                'current_password': 'Current password is incorrect'
            })

        return data

class ChangeEmailSerializer(serializers.Serializer):
    """Serializer for email change with password confirmation"""
    new_email = serializers.EmailField()
    current_password = serializers.CharField()

    def validate(self, data):
        """Check if email is already taken and verify password"""
        user = self.context.get('user')
        new_email = data['new_email']

        # Check if email is already taken by another user
        if User.objects.filter(email=new_email).exclude(id=user.id).exists():
            raise serializers.ValidationError({
                'new_email': 'This email is already registered'
            })

        # Verify current password
        if not verify_password(data['current_password'], user.password_hash):
            raise serializers.ValidationError({
                'current_password': 'Current password is incorrect'
            })

        return data

class DeleteAccountSerializer(serializers.Serializer):
    """Serializer for account deletion with password confirmation"""
    current_password = serializers.CharField()
    confirm_deletion = serializers.BooleanField()

    def validate_confirm_deletion(self, value):
        """Ensure user explicitly confirms deletion"""
        if not value:
            raise serializers.ValidationError(
                "You must confirm account deletion"
            )
        return value

    def validate(self, data):
        """Verify current password before allowing deletion"""
        user = self.context.get('user')

        # Verify current password
        if not verify_password(data['current_password'], user.password_hash):
            raise serializers.ValidationError({
                'current_password': 'Current password is incorrect'
            })

        return data

class UserMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMetrics
        fields = '__all__'

class UserMetricsCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating user metrics without user field"""
    class Meta:
        model = UserMetrics
        fields = ['date_recorded', 'weight_kg', 'height_cm', 'activity_level']

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['id', 'user', 'title', 'description', 'goal_type', 'target_weight_kg', 
                  'target_date', 'start_date', 'end_date', 'status', 'is_active', 
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class GoalCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating goals without user field"""
    class Meta:
        model = Goal
        fields = ['title', 'description', 'goal_type', 'target_weight_kg', 
                  'target_date', 'start_date', 'end_date', 'status']

# -------------------------------
# Exercise & Workout Serializers
# -------------------------------

class WorkoutPlanDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutPlan
        fields = '__all__'

class WorkoutPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutPlan
        fields = '__all__'

class WorkoutLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutLog
        fields = '__all__'

class WorkoutPlanCompletionLogSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    workout_plan_name = serializers.CharField(source='workout_plan.name', read_only=True)
    
    class Meta:
        model = WorkoutPlanCompletionLog
        fields = '__all__'


# -------------------------------
# Nutrition Serializers
# -------------------------------
class NutritionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = NutritionLog
        fields = ['id', 'user', 'food_name', 'date_eaten', 'quantity', 'meal_type', 'calories', 'protein', 'carbs', 'sugar']

# -------------------------------
# Meal Plan Serializers
# -------------------------------
class MealPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealPlan
        fields = '__all__'


class MealPlanDetailSerializer(serializers.ModelSerializer):
    """Complete detailed serializer for meal plans with all nested data."""
    
    class Meta:
        model = MealPlan
        fields = ['id', 'name', 'description', 'created_at', 'user', 'meal_plan_data', 'daily_calorie_target', 'days_count', 'dietary_preferences', 'goal']
