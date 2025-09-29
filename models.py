from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class User(AbstractUser):
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    login_streak = models.PositiveIntegerField(default=0)
    last_login_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class UserMetrics(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    ACTIVITY_LEVEL_CHOICES = [
        ('sedentary', 'Sedentary (little/no exercise)'),
        ('lightly_active', 'Lightly active (light exercise 1-3 days/week)'),
        ('moderately_active', 'Moderately active (moderate exercise 3-5 days/week)'),
        ('very_active', 'Very active (hard exercise 6-7 days/week)'),
        ('extra_active', 'Extra active (very hard exercise, physical job)'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='metrics')
    age = models.PositiveIntegerField(validators=[MinValueValidator(13), MaxValueValidator(120)])
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2)
    height_cm = models.DecimalField(max_digits=5, decimal_places=2)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_LEVEL_CHOICES)
    date_recorded = models.DateTimeField(auto_now_add=True)

    def calculate_bmr(self):
        """Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation"""
        if self.gender == 'M':
            return (10 * float(self.weight_kg)) + (6.25 * float(self.height_cm)) - (5 * self.age) + 5
        else:
            return (10 * float(self.weight_kg)) + (6.25 * float(self.height_cm)) - (5 * self.age) - 161

    def calculate_tdee(self):
        """Calculate Total Daily Energy Expenditure"""
        bmr = self.calculate_bmr()
        activity_multipliers = {
            'sedentary': 1.2,
            'lightly_active': 1.375,
            'moderately_active': 1.55,
            'very_active': 1.725,
            'extra_active': 1.9
        }
        return bmr * activity_multipliers.get(self.activity_level, 1.2)

class Goals(models.Model):
    GOAL_TYPE_CHOICES = [
        ('weight_loss', 'Weight Loss'),
        ('weight_gain', 'Weight Gain'),
        ('muscle_gain', 'Muscle Gain'),
        ('maintenance', 'Maintenance'),
        ('activity', 'Activity Goal'),
        ('nutrition', 'Nutrition Goal'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')
    goal_type = models.CharField(max_length=20, choices=GOAL_TYPE_CHOICES)
    target_weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    target_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    target_date = models.DateField(null=True, blank=True)
    start_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
