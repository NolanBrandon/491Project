from django.contrib import admin
from .models import WorkoutPlan

@admin.register(WorkoutPlan)
class WorkoutPlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user')
    list_filter = ('created_at',)
    search_fields = ('name', 'user__username')

