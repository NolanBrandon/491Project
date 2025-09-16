from django.db import models
from django.contrib.auth.models import User

# User profile to store additional info
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    gender = models.CharField(max_length=10, blank=True)
    activity_level = models.CharField(max_length=50, blank=True)  # e.g., sedentary, active

    def __str__(self):
        return self.user.username

# Goals (e.g., weight loss, muscle gain)
class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal_type = models.CharField(max_length=50)  # 'weight_loss', 'muscle_gain', etc.
    target_value = models.FloatField()           # e.g., target weight
    deadline = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.goal_type}"

# Exercise model
class Exercise(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    calories_burned_per_minute = models.FloatField(default=0.0)
    muscle_groups = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

# Workout plan
class Workout(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    exercises = models.ManyToManyField(Exercise, through='WorkoutExercise')

    def __str__(self):
        return self.name

# Through model for workouts and exercises
class WorkoutExercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    duration_minutes = models.PositiveIntegerField(default=10)

# Workout sessions by user
class WorkoutSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    duration_minutes = models.PositiveIntegerField(default=0)
    calories_burned = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.user.username} - {self.workout.name} on {self.date.date()}"

# Diet model
class DietPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    calories_per_day = models.PositiveIntegerField(default=2000)

    def __str__(self):
        return f"{self.user.username} - {self.name}"

# Meals within DietPlan
class Meal(models.Model):
    diet_plan = models.ForeignKey(DietPlan, on_delete=models.CASCADE, related_name="meals")
    name = models.CharField(max_length=100)
    calories = models.PositiveIntegerField()
    protein_grams = models.FloatField(default=0)
    carbs_grams = models.FloatField(default=0)
    fats_grams = models.FloatField(default=0)

    def __str__(self):
        return f"{self.diet_plan.name} - {self.name}"
