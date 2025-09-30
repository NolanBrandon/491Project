from django.contrib import admin
from .models import Exercise, WorkoutPlan, PlanDay, PlanExercise

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(WorkoutPlan)
class WorkoutPlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(PlanDay)
class PlanDayAdmin(admin.ModelAdmin):
    list_display = ('id', 'plan', 'day')

@admin.register(PlanExercise)
class PlanExerciseAdmin(admin.ModelAdmin):
    list_display = ('id', 'plan_day', 'exercise', 'sets', 'reps')

