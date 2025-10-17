from django.db import models
from django.core.exceptions import ValidationError
import uuid

# -------------------------------
# User Management & Core Tracking Module
# -------------------------------

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=50, unique=True, default='')
    email = models.EmailField(max_length=255, unique=True, default='')
    password_hash = models.CharField(max_length=255, default='')
    gender = models.CharField(max_length=50, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    last_login_date = models.DateField(null=True, blank=True)
    login_streak = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username


class UserMetrics(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_recorded = models.DateField()
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    height_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    activity_level = models.CharField(max_length=50, null=True, blank=True)
    
    class Meta:
        db_table = 'user_metrics'

    def __str__(self):
        return f"{self.user.username} metrics on {self.date_recorded}"


class Goal(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('paused', 'Paused'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default='')
    description = models.TextField(blank=True, default='')
    goal_type = models.CharField(max_length=50, default='', blank=True)
    target_weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    target_date = models.DateField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'goals'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"


# -------------------------------
# Exercise & Workout Module
# -------------------------------


class WorkoutPlan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='')
    description = models.TextField(null=True, blank=True)
    workout_plan_data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    class Meta:
        db_table = 'workout_plans'

    def __str__(self):
        return self.name


class WorkoutLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise_name = models.CharField(max_length=255, default='')
    date_performed = models.DateTimeField(auto_now_add=True)
    sets_performed = models.IntegerField(default=1)
    reps_performed = models.IntegerField(default=1)
    duration_minutes = models.IntegerField(null=True, blank=True)
    calories_burned = models.IntegerField(null=True, blank=True)
    perceived_effort = models.IntegerField(null=True, blank=True)  # RPE scale 1-10

    class Meta:
        db_table = 'workout_log'

    def __str__(self):
        return f"{self.user.username} - {self.exercise_name} on {self.date_performed.date()}"


# -------------------------------
# Nutrition & Meal Planning Module
# -------------------------------

class NutritionLog(models.Model):
    MEAL_TYPE_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_name = models.CharField(max_length=255, default='')
    date_eaten = models.DateTimeField()
    quantity = models.DecimalField(max_digits=5, decimal_places=2, default=1.0)  # Multiplier of serving size
    meal_type = models.CharField(max_length=50, choices=MEAL_TYPE_CHOICES, null=True, blank=True)

    # Nutritional information fields
    calories = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    protein = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)  # grams
    carbs = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)  # grams

    class Meta:
        db_table = 'nutrition_log'

    def __str__(self):
        return f"{self.user.username} - {self.food_name} on {self.date_eaten.date()}"


class MealPlan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='')
    description = models.TextField(null=True, blank=True)
    
    # Store complete AI-generated meal plan data as JSON
    meal_plan_data = models.JSONField(default=dict, help_text="Complete meal plan with days, meals, recipes, ingredients, and nutritional data")
    
    # Metadata fields for easy filtering and searching
    daily_calorie_target = models.IntegerField(null=True, blank=True)
    days_count = models.IntegerField(null=True, blank=True)
    dietary_preferences = models.JSONField(default=list, help_text="List of dietary preferences")
    goal = models.CharField(max_length=100, blank=True, help_text="User's fitness/nutrition goal")
    
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    class Meta:
        db_table = 'meal_plans'

    def __str__(self):
        return self.name