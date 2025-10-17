from rest_framework import serializers
from decimal import Decimal
from .models import NutritionLog, FoodDatabase
from .services import OpenFoodFactsService, MacroCalculatorService

class NutritionLogSerializer(serializers.ModelSerializer):
    food_name = serializers.CharField(source='food.name', read_only=True, required=False)
    food_brand = serializers.CharField(source='food.brand', read_only=True, required=False)
    
    
    class Meta:
        model = NutritionLog
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')
    
     def validate(self, data):
        numeric_fields = ['calories', 'protein', 'carbs', 'fat', 'fiber', 'sugar', 'sodium']
        
        for field in numeric_fields:
            value = data.get(field)
            if value is not None and value < 0:
                raise serializers.ValidationError({
                    field: f"{field.capitalize()} cannot be negative"
                })
        
        return data

class BarcodeSearchSerializer(serializers.Serializer):
    barcode = serializers.CharField(max_length=50)
    quantity = serializers.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        default=100,
        min_value=0.01  
        help_text="Quantity in grams"
    ) 
    
    def validate_barcode(self, value):
         value = value.strip()      
        if not value.isdigit():
            raise serializers.ValidationError("Barcode must contain only numbers")
        if len(value) not in [8, 12, 13, 14]:
            raise serializers.ValidationError(
                "Barcode must be 8, 12, 13, or 14 digits long"
            )
        
        return value
    
    def validate_quantity(self, value):
        if value > 10000:  # 10kg seems like a reasonable maximum
            raise serializers.ValidationError(
                "Quantity cannot exceed 10,000 grams (10kg)"
            )
        return value
    
    def create(self, validated_data):
        barcode = validated_data['barcode']
        quantity = validated_data['quantity']
        product_data = OpenFoodFactsService.get_product_by_barcode(barcode)
        
        if 'error' in product_data:
            raise serializers.ValidationError({
                'barcode': product_data['error']
            })
        
        nutrition_data = MacroCalculatorService.calculate_nutrition_for_quantity(
            product_data['nutrition_per_100g'],
            float(quantity)
        )
    
        return {
            'barcode': product_data['barcode'],
            'name': product_data['name'],
            'brand': product_data['brand'],
            'quantity_g': float(quantity),
            'nutrition_per_100g': product_data['nutrition_per_100g'],
            'nutrition_total': nutrition_data
        }


class BarcodeSearchResponseSerializer(serializers.Serializer):
    barcode = serializers.CharField()
    name = serializers.CharField()
    brand = serializers.CharField()
    quantity_g = serializers.DecimalField(max_digits=8, decimal_places=2)
    nutrition_per_100g = serializers.DictField()
    nutrition_total = serializers.DictField()


class CreateNutritionLogFromBarcodeSerializer(serializers.Serializer):
    barcode = serializers.CharField(max_length=50)
    quantity = serializers.DecimalField(
        max_digits=8, 
        decimal_places=2,
        min_value=0.01,
        help_text="Quantity in grams"
    )
    meal_type = serializers.ChoiceField(
        choices=NutritionLog.MEAL_TYPE_CHOICES,
        required=False
    )
    notes = serializers.CharField(max_length=500, required=False, allow_blank=True)
    
    def validate_barcode(self, value):
        value = value.strip()
        if not value.isdigit():
            raise serializers.ValidationError("Barcode must contain only numbers")
        if len(value) not in [8, 12, 13, 14]:
            raise serializers.ValidationError("Invalid barcode length")
        return value
    
    def create(self, validated_data):
        barcode = validated_data['barcode']
        quantity = validated_data['quantity']
        user = self.context['request'].user

        try:
            food = FoodDatabase.objects.get(barcode=barcode)
            food_data = {
                'name': food.name,
                'brand': food.brand or '',
                'nutrition_per_100g': {
                    'calories': float(food.calories_per_100g),
                    'protein': float(food.protein_per_100g),
                    'carbohydrates': float(food.carbs_per_100g),
                    'fat': float(food.fat_per_100g),
                    'fiber': float(food.fiber_per_100g),
                    'sugar': float(food.sugar_per_100g),
                    'sodium': float(food.sodium_per_100g),
                }
            }
        except FoodDatabase.DoesNotExist:
            product_data = OpenFoodFactsService.get_product_by_barcode(barcode)
            
            if 'error' in product_data:
                raise serializers.ValidationError({'barcode': product_data['error']})
           
            FoodDatabase.objects.create(
                barcode=barcode,
                name=product_data['name'],
                brand=product_data.get('brand', ''),
                calories_per_100g=product_data['nutrition_per_100g']['calories'],
                protein_per_100g=product_data['nutrition_per_100g']['protein'],
                carbs_per_100g=product_data['nutrition_per_100g']['carbohydrates'],
                fat_per_100g=product_data['nutrition_per_100g']['fat'],
                fiber_per_100g=product_data['nutrition_per_100g'].get('fiber', 0),
                sugar_per_100g=product_data['nutrition_per_100g'].get('sugar', 0),
                sodium_per_100g=product_data['nutrition_per_100g'].get('sodium', 0),
            )
            food_data = product_data
        
        
        nutrition = MacroCalculatorService.calculate_nutrition_for_quantity(
            product_data['nutrition_per_100g'],
            float(quantity)
        )
        
        food, _ = FoodDatabase.objects.get_or_create(barcode=barcode)
        
        log = NutritionLog.objects.create(
            user=user,
            food_item=food_data['name'],
            barcode=barcode,
            quantity=quantity,
            unit='g',
            meal_type=validated_data.get('meal_type', 'snack'),
            calories=Decimal(str(nutrition['calories'])),
            protein_g=Decimal(str(nutrition['protein'])),
            carbohydrates_g=Decimal(str(nutrition['carbohydrates'])),
            fat_g=Decimal(str(nutrition['fat'])),
            fiber_g=Decimal(str(nutrition.get('fiber', 0))),
            sugar_g=Decimal(str(nutrition.get('sugar', 0))),
            sodium_mg=Decimal(str(nutrition.get('sodium', 0))),
        )
        
        return log
        
class FoodDatabaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodDatabase
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class NutritionSummarySerializer(serializers.Serializer):
    date = serializers.DateField(required=False)
    total_calories = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_protein = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_carbs = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_fat = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_fiber = serializers.DecimalField(max_digits=10, decimal_places=2)
    meal_count = serializers.IntegerField()
