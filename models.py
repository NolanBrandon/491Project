from django.contrib.auth.models import AbstractUser
from django.db import models

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class Meta:
        db_table = 'auth_user'

class UserProfile(models.Model):
    """Extended user profile information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'api_userprofile'

class UserMetrics(models.Model):
    """User physical metrics for fitness calculations"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metrics')
    weight = models.FloatField(help_text="Weight in kg")
    height = models.FloatField(help_text="Height in cm")
    age = models.IntegerField()
    
    class Meta:
        db_table = 'user_metrics'
    
    def calculate_bmr(self):
        """Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation"""
        # Need gender info - you may need to add this field or get it from profile
        # For now, using gender-neutral calculation
        return (10 * self.weight) + (6.25 * self.height) - (5 * self.age)

class Goals(models.Model):
    """User fitness and health goals"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')
    goal_type = models.CharField(max_length=50)
    target_value = models.FloatField(null=True, blank=True)
    
    class Meta:
        db_table = 'goals'
        verbose_name_plural = 'Goals'
