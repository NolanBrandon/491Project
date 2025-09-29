from django.db import models
from django.contrib.auth.models import User

class NutritionLog(models.Model):
    MEAL_TYPE_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='nutrition_logs')
    food_item = models.CharField(max_length=255)
    barcode = models.CharField(max_length=50, null=True, blank=True)
    quantity = models.DecimalField(max_digits=8, decimal_places=2)
    unit = models.CharField(max_length=20, default='g')
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPE_CHOICES)
    date_eaten = models.DateTimeField(auto_now_add=True)

    # Nutritional Information
    calories = models.DecimalField(max_digits=7, decimal_places=2)
    protein_g = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    carbohydrates_g = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    fat_g = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    fiber_g = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    sugar_g = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    sodium_mg = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    
    # Vitamins and minerals (per 100g)
    vitamin_d_mcg = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    vitamin_c_mg = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    calcium_mg = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    iron_mg = models.DecimalField(max_digits=6, decimal_places=2, default=0)

class FoodDatabase(models.Model):
    """Cache for food items fetched from Open Food Facts API"""
    barcode = models.CharField(max_length=50, unique=True, db_index=True)
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255, null=True, blank=True)
    
    # Nutritional values per 100g
    calories_per_100g = models.DecimalField(max_digits=7, decimal_places=2)
    protein_per_100g = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    carbs_per_100g = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    fat_per_100g = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    fiber_per_100g = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    sugar_per_100g = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    sodium_per_100g = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
