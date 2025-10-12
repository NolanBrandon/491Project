from rest_framework import serializers
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
        fields = ['id', 'username', 'email', 'gender', 'date_of_birth', 'last_login_date', 'login_streak', 'created_at']

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

class IngredientSerializer(serializers.ModelSerializer):
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
