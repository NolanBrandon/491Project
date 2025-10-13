from rest_framework import serializers
import hashlib
import secrets
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
)

def hash_password(password):
    """Simple password hashing using SHA-256 with salt"""
    salt = secrets.token_hex(16)
    hashed = hashlib.sha256((password + salt).encode()).hexdigest()
    return f"{salt}${hashed}"

def verify_password(password, hashed_password):
    """Verify password against hash"""
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

class UserMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMetrics
        fields = '__all__'

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = '__all__'

# -------------------------------
# Exercise & Workout Serializers
# -------------------------------
class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = '__all__'

class MuscleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Muscle
        fields = '__all__'

class ExerciseMuscleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseMuscle
        fields = '__all__'

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = '__all__'

class ExerciseEquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseEquipment
        fields = '__all__'

class BodyPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = BodyPart
        fields = '__all__'

class ExerciseBodyPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseBodyPart
        fields = '__all__'

class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = '__all__'

class ExerciseKeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseKeyword
        fields = '__all__'

class RelatedExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelatedExercise
        fields = '__all__'

class PlanExerciseDetailSerializer(serializers.ModelSerializer):
    exercise = ExerciseSerializer(read_only=True)
    
    class Meta:
        model = PlanExercise
        fields = '__all__'

class PlanDayDetailSerializer(serializers.ModelSerializer):
    plan_exercises = PlanExerciseDetailSerializer(many=True, read_only=True)
    
    class Meta:
        model = PlanDay
        fields = '__all__'

class WorkoutPlanDetailSerializer(serializers.ModelSerializer):
    plan_days = PlanDayDetailSerializer(many=True, read_only=True)
    
    class Meta:
        model = WorkoutPlan
        fields = '__all__'

class WorkoutPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutPlan
        fields = '__all__'

class PlanDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanDay
        fields = '__all__'

class PlanExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanExercise
        fields = '__all__'

class WorkoutLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutLog
        fields = '__all__'

# -------------------------------
# Nutrition Serializers
# -------------------------------
class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'

class NutritionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = NutritionLog
        fields = '__all__'

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
