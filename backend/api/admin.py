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