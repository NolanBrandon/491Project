from rest_framework import serializers
from .models import NutritionLog
from .services import OpenFoodFactsService, MacroCalculatorService

class NutritionLogSerializer(serializers.ModelSerializer):
    calories = serializers.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        read_only=True,
        required=False
    )
    
    class Meta:
        model = NutritionLog
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')  # Add timestamp fields if they exist
    
    def validate(self, data):
        if data.get('protein', 0) < 0 or data.get('carbs', 0) < 0 or data.get('fat', 0) < 0:
            raise serializers.ValidationError("Macro values must be non-negative")
        return data


class BarcodeSearchSerializer(serializers.Serializer):
    barcode = serializers.CharField(max_length=50)
    quantity = serializers.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        default=100,
        min_value=0.01  # Prevent zero or negative quantities
    )
    
    def validate_barcode(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Barcode must contain only numbers")
        if len(value) not in [8, 12, 13, 14]:
            raise serializers.ValidationError(
                "Barcode must be 8, 12, 13, or 14 digits long"
            )
        
        return value
    
    def validate(self, data):  
        barcode = data.get('barcode')
        product = OpenFoodFactsService.get_product(barcode)
        if not product:
             raise serializers.ValidationError(
                 {"barcode": "Product not found in database"}
             )
        return data


class MacroCalculatorSerializer(serializers.Serializer):
    weight = serializers.DecimalField(max_digits=5, decimal_places=2, min_value=1)
    height = serializers.DecimalField(max_digits=5, decimal_places=2, min_value=1)
    age = serializers.IntegerField(min_value=1, max_value=120)
    gender = serializers.ChoiceField(choices=['male', 'female', 'other'])
    activity_level = serializers.ChoiceField(
        choices=['sedentary', 'light', 'moderate', 'active', 'very_active']
    )
    goal = serializers.ChoiceField(
        choices=['lose', 'maintain', 'gain']
    )
