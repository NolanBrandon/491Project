from django.db import models
from django.contrib.auth.models import User

# -------------------------------
# User & Metrics
# -------------------------------

class UserMetrics(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    weight = models.FloatField(null=True, blank=True, default=1.0)
    height = models.FloatField(null=True, blank=True, default=1.0)
    age = models.IntegerField(null=True, blank=True, default=1)
    
    class Meta:
        db_table = 'user_metrics'


class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    goal_type = models.CharField(max_length=255, default='General')
    target_value = models.FloatField(null=True, blank=True, default=1.0)
    
    class Meta:
        db_table = 'goals'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    bio = models.TextField(blank=True, default='')
    
    class Meta:
        db_table = 'api_userprofile'


# -------------------------------
# Nutrition / Diet
# -------------------------------

class Food(models.Model):
    name = models.CharField(max_length=255, default='Food')
    calories = models.FloatField(default=0.0)
    
    class Meta:
        db_table = 'foods'


class NutritionLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    food = models.ForeignKey(Food, on_delete=models.CASCADE, default=1)
    amount = models.FloatField(default=1.0)
    
    class Meta:
        db_table = 'nutrition_log'


class MealPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=255, default='Meal Plan')
    
    class Meta:
        db_table = 'meal_plans'


class MealPlanDay(models.Model):
    plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE, default=1)
    day = models.IntegerField(default=1)
    
    class Meta:
        db_table = 'meal_plan_days'


class MealPlanEntry(models.Model):
    meal_day = models.ForeignKey(MealPlanDay, on_delete=models.CASCADE, default=1)
    food = models.ForeignKey(Food, on_delete=models.CASCADE, default=1)
    quantity = models.FloatField(default=1.0)
    
    class Meta:
        db_table = 'meal_plan_entries'


class Recipe(models.Model):
    name = models.CharField(max_length=255, default='Recipe')
    
    class Meta:
        db_table = 'recipes'


class Ingredient(models.Model):
    name = models.CharField(max_length=255, default='Ingredient')
    
    class Meta:
        db_table = 'ingredients'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, default=1)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, default=1)
    quantity = models.FloatField(default=1.0)
    
    class Meta:
        db_table = 'recipe_ingredients'


class Tag(models.Model):
    name = models.CharField(max_length=255, default='Tag')
    
    class Meta:
        db_table = 'tags'


class RecipeTag(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, default=1)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, default=1)
    
    class Meta:
        db_table = 'recipe_tags'


# -------------------------------
# Exercise / Workout
# -------------------------------

class Exercise(models.Model):
    name = models.CharField(max_length=255, default='Exercise')
    
    class Meta:
        db_table = 'exercises'


class WorkoutPlan(models.Model):
    name = models.CharField(max_length=255, default='Workout Plan')
    
    class Meta:
        db_table = 'workout_plans'


class PlanDay(models.Model):
    plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE, default=1)
    day = models.IntegerField(default=1)
    
    class Meta:
        db_table = 'plan_days'
        unique_together = ('plan', 'day')


class PlanExercise(models.Model):
    plan_day = models.ForeignKey(PlanDay, on_delete=models.CASCADE, default=1)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, default=1)
    sets = models.IntegerField(default=1)
    reps = models.IntegerField(default=1)
    
    class Meta:
        db_table = 'plan_exercises'


class Equipment(models.Model):
    name = models.CharField(max_length=255, default='Equipment')
    
    class Meta:
        db_table = 'equipments'


class ExerciseEquipment(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, default=1)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, default=1)
    
    class Meta:
        db_table = 'exercise_equipments'


class BodyPart(models.Model):
    name = models.CharField(max_length=255, default='Body Part')
    
    class Meta:
        db_table = 'body_parts'


class ExerciseBodyPart(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, default=1)
    body_part = models.ForeignKey(BodyPart, on_delete=models.CASCADE, default=1)
    
    class Meta:
        db_table = 'exercise_body_parts'


class Muscle(models.Model):
    name = models.CharField(max_length=255, default='Muscle')
    
    class Meta:
        db_table = 'muscles'


class ExerciseMuscle(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, default=1)
    muscle = models.ForeignKey(Muscle, on_delete=models.CASCADE, default=1)
    
    class Meta:
        db_table = 'exercise_muscles'


class Keyword(models.Model):
    word = models.CharField(max_length=255, default='Keyword')
    
    class Meta:
        db_table = 'keywords'


class ExerciseKeyword(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, default=1)
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE, default=1)
    
    class Meta:
        db_table = 'exercise_keywords'


class RelatedExercise(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='main_exercise', default=1)
    related = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='related_exercise', default=1)
    
    class Meta:
        db_table = 'related_exercises'
