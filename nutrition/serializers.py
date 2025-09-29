from rest_framework import serializers
from .models import NutritionLog, FoodDatabase

class NutritionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = NutritionLog
        fields = [
            'id', 'food_item', 'barcode', 'quantity', 'unit', 
            'meal_type', 'date_eaten', 'calories', 'protein_g',
            'carbohydrates_g', 'fat_g', 'fiber_g', 'sugar_g',
            'sodium_mg', 'vitamin_d_mcg', 'vitamin_c_mg',
            'calcium_mg', 'iron_mg'
        ]
        read_only_fields = ['id', 'date_eaten']

class FoodDatabaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodDatabase
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
