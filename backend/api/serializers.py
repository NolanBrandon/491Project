from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    UserMetrics,
    Goal,
    Exercise,
    WorkoutPlan,
    PlanDay,
    PlanExercise,
    Ingredient,
    RecipeIngredient,
    Food,
    NutritionLog,
    MealPlan,
    MealPlanDay,
    Recipe,
    MealPlanEntry,
    Tag,
    RecipeTag
)

# -------------------------------
# User Serializers
# -------------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

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
# Meal Plan & Recipe Serializers
# -------------------------------
class MealPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealPlan
        fields = '__all__'

class MealPlanDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = MealPlanDay
        fields = '__all__'

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'

class MealPlanEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = MealPlanEntry
        fields = '__all__'

class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'

class RecipeIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeIngredient
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class RecipeTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeTag
        fields = '__all__'
