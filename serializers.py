from rest_framework import serializers
from .models import NutritionLog
from .services import OpenFoodFactsService, MacroCalculatorService

class NutritionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = NutritionLog
        fields = '__all__'
        read_only_fields = ('user',)

class BarcodeSearchSerializer(serializers.Serializer):
    barcode = serializers.CharField(max_length=50)
    quantity = serializers.DecimalField(max_digits=8, decimal_places=2, default=100)

    def validate_barcode(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Barcode must contain only numbers")
        return value
