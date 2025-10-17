from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone


class NutritionEntry(models.Model):
    """Model for individual nutrition entries"""
    
    MEAL_TYPES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='nutrition_entries')
    food_name = models.CharField(max_length=255)
    serving_size = models.FloatField(validators=[MinValueValidator(0.0)])
    serving_unit = models.CharField(max_length=50, default='serving')
    
    # Calories
    calories = models.FloatField(validators=[MinValueValidator(0.0)])
    
    # Macronutrients (in grams)
    protein = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    carbohydrates = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    fats = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    fiber = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    sugar = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    
    # Micronutrients (in mg unless specified)
    vitamin_d = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)], help_text="mcg")
    vitamin_c = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)], help_text="mg")
    calcium = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)], help_text="mg")
    iron = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)], help_text="mg")
    magnesium = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)], help_text="mg")
    sodium = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)], help_text="mg")
    potassium = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)], help_text="mg")
    
    # Metadata
    timestamp = models.DateTimeField(default=timezone.now)
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPES, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    
    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Nutrition Entry'
        verbose_name_plural = 'Nutrition Entries'
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['user', 'meal_type']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.food_name} ({self.timestamp.date()})"
    
    def get_macro_calories(self):
        """Calculate calories from macronutrients"""
        return {
            'protein_calories': self.protein * 4,
            'carb_calories': self.carbohydrates * 4,
            'fat_calories': self.fats * 9,
            'total_macro_calories': (self.protein * 4) + (self.carbohydrates * 4) + (self.fats * 9)
        }


class DailyNutritionGoal(models.Model):
    """Model for user's daily nutrition goals"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='nutrition_goals')
    
    # Calorie goals
    calories = models.FloatField(validators=[MinValueValidator(0.0)])
    
    # Macronutrient goals (in grams)
    protein = models.FloatField(validators=[MinValueValidator(0.0)])
    carbohydrates = models.FloatField(validators=[MinValueValidator(0.0)])
    fats = models.FloatField(validators=[MinValueValidator(0.0)])
    fiber = models.FloatField(default=25.0, validators=[MinValueValidator(0.0)])
    sugar = models.FloatField(default=50.0, validators=[MinValueValidator(0.0)])
    
    # Micronutrient goals
    vitamin_d = models.FloatField(default=20.0, validators=[MinValueValidator(0.0)], help_text="mcg")
    vitamin_c = models.FloatField(default=75.0, validators=[MinValueValidator(0.0)], help_text="mg")
    calcium = models.FloatField(default=1000.0, validators=[MinValueValidator(0.0)], help_text="mg")
    iron = models.FloatField(default=18.0, validators=[MinValueValidator(0.0)], help_text="mg")
    magnesium = models.FloatField(default=320.0, validators=[MinValueValidator(0.0)], help_text="mg")
    sodium = models.FloatField(default=2300.0, validators=[MinValueValidator(0.0)], help_text="mg")
    potassium = models.FloatField(default=2600.0, validators=[MinValueValidator(0.0)], help_text="mg")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Daily Nutrition Goal'
        verbose_name_plural = 'Daily Nutrition Goals'
    
    def __str__(self):
        return f"{self.user.username}'s Nutrition Goals"
    
    def get_macro_percentages(self):
        """Calculate recommended macro percentages"""
        protein_cals = self.protein * 4
        carb_cals = self.carbohydrates * 4
        fat_cals = self.fats * 9
        total_cals = protein_cals + carb_cals + fat_cals
        
        if total_cals == 0:
            return {'protein': 0, 'carbohydrates': 0, 'fats': 0}
        
        return {
            'protein': round((protein_cals / total_cals) * 100, 1),
            'carbohydrates': round((carb_cals / total_cals) * 100, 1),
            'fats': round((fat_cals / total_cals) * 100, 1)
        }


class FoodItem(models.Model):
    """Model for storing common food items (database)"""
    
    name = models.CharField(max_length=255, unique=True)
    barcode = models.CharField(max_length=50, blank=True, null=True, unique=True)
    brand = models.CharField(max_length=255, blank=True, null=True)
    
    # Default serving information
    default_serving_size = models.FloatField(validators=[MinValueValidator(0.0)])
    serving_unit = models.CharField(max_length=50, default='serving')
    
    # Nutritional information per serving
    calories = models.FloatField(validators=[MinValueValidator(0.0)])
    protein = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    carbohydrates = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    fats = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    fiber = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    sugar = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    
    # Micronutrients
    vitamin_d = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    vitamin_c = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    calcium = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    iron = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    magnesium = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    sodium = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    potassium = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    
    # Metadata
    source = models.CharField(max_length=100, blank=True, help_text="e.g., OpenFoodFacts, USDA")
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Food Item'
        verbose_name_plural = 'Food Items'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['barcode']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.brand or 'Generic'})"
    
    def create_nutrition_entry(self, user, servings=1.0, meal_type=None, notes=None):
        """Create a nutrition entry from this food item"""
        return NutritionEntry.objects.create(
            user=user,
            food_name=self.name,
            serving_size=servings * self.default_serving_size,
            serving_unit=self.serving_unit,
            calories=self.calories * servings,
            protein=self.protein * servings,
            carbohydrates=self.carbohydrates * servings,
            fats=self.fats * servings,
            fiber=self.fiber * servings,
            sugar=self.sugar * servings,
            vitamin_d=self.vitamin_d * servings,
            vitamin_c=self.vitamin_c * servings,
            calcium=self.calcium * servings,
            iron=self.iron * servings,
            magnesium=self.magnesium * servings,
            sodium=self.sodium * servings,
            potassium=self.potassium * servings,
            meal_type=meal_type,
            notes=notes
        )
