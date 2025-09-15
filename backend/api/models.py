from django.db import models

# Create your models here.

# Example model structure for future development:
# 
# class User(models.Model):
#     username = models.CharField(max_length=150, unique=True)
#     email = models.EmailField(unique=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
# class WorkoutPlan(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=200)
#     description = models.TextField(blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#
# class Exercise(models.Model):
#     name = models.CharField(max_length=200)
#     description = models.TextField(blank=True)
#     muscle_group = models.CharField(max_length=100)
#     equipment_needed = models.CharField(max_length=200, blank=True)
#
# class WorkoutSession(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     workout_plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE)
#     date = models.DateTimeField(auto_now_add=True)
#     duration_minutes = models.PositiveIntegerField()
#     calories_burned = models.PositiveIntegerField(null=True, blank=True)