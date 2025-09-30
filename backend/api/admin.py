from django.contrib import admin

# Register your models here.

# Example admin registrations for future development:
# from .models import User, WorkoutPlan, Exercise, WorkoutSession
#
# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('username', 'email', 'created_at')
#     search_fields = ('username', 'email')
#
# @admin.register(WorkoutPlan)
# class WorkoutPlanAdmin(admin.ModelAdmin):
#     list_display = ('name', 'user', 'created_at')
#     list_filter = ('created_at',)
#
# @admin.register(Exercise)
# class ExerciseAdmin(admin.ModelAdmin):
#     list_display = ('name', 'muscle_group', 'equipment_needed')
#     list_filter = ('muscle_group',)
#
# @admin.register(WorkoutSession)
# class WorkoutSessionAdmin(admin.ModelAdmin):
#     list_display = ('user', 'workout_plan', 'date', 'duration_minutes')
#     list_filter = ('date',)

from django.contrib import admin
from .models import Workout, Exercise, WorkoutExercise, WorkoutSession

@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)  # Only include existing fields

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'calories_burned_per_minute', 'muscle_groups')

@admin.register(WorkoutExercise)
class WorkoutExerciseAdmin(admin.ModelAdmin):
    list_display = ('id', 'workout', 'exercise', 'duration_minutes')

@admin.register(WorkoutSession)
class WorkoutSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'workout', 'date', 'duration_minutes', 'calories_burned')

