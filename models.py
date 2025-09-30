from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class Meta:
        db_table = 'auth_user'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'api_userprofile'

class UserMetrics(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metrics', db_column='user_id')
    weight = models.FloatField(help_text="Weight in kg")
    height = models.FloatField(help_text="Height in cm")
    age = models.IntegerField()
    
    class Meta:
        db_table = 'user_metrics'
        verbose_name_plural = 'User Metrics'
    
    def calculate_bmr(self):
        return (10 * self.weight) + (6.25 * self.height) - (5 * self.age)

    def __str__(self):
        return f"{self.user.username} - {self.weight}kg, {self.height}cm, {self.age}y"

class Goals(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals', db_column='user_id')
    goal_type = models.CharField(max_length=50)
    target_value = models.FloatField(null=True, blank=True)
    
    class Meta:
        db_table = 'goals'
        verbose_name_plural = 'Goals'

    def __str__(self):
        return f"{self.user.username} - {self.goal_type}: {self.target_value}"
