from rest_framework import serializers
from .models import UserProfile, Exercise, Workout, WorkoutExercise, WorkoutSession, Goal, DietPlan, Meal
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = UserProfile
        fields = ['user', 'age', 'weight', 'height', 'gender', 'activity_level']

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = '__all__'

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = '__all__'

class WorkoutSerializer(serializers.ModelSerializer):
    exercises = ExerciseSerializer(many=True, read_only=True)
    class Meta:
        model = Workout
        fields = ['id', 'name', 'description', 'exercises']

class WorkoutSessionSerializer(serializers.ModelSerializer):
    workout = WorkoutSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = WorkoutSession
        fields = ['id', 'user', 'workout', 'date', 'duration_minutes', 'calories_burned']

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = '__all__'

class DietPlanSerializer(serializers.ModelSerializer):
    meals = MealSerializer(many=True, read_only=True)
    class Meta:
        model = DietPlan
        fields = ['id', 'user', 'name', 'description', 'calories_per_day', 'meals']
