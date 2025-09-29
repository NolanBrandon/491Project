from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum, Q
from datetime import date, timedelta
from .models import NutritionLog
from .serializers import NutritionLogSerializer, BarcodeSearchSerializer
from .services import OpenFoodFactsService, MacroCalculatorService

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def scan_barcode(request):
    """Scan barcode and return nutritional information"""
    serializer = BarcodeSearchSerializer(data=request.data)
    if serializer.is_valid():
        barcode = serializer.validated_data['barcode']
        quantity = serializer.validated_data['quantity']
        
        food_data = OpenFoodFactsService.get_product_by_barcode(barcode)
        
        if 'error' in food_data:
            return Response(food_data, status=status.HTTP_404_NOT_FOUND)
        
        nutrition_for_quantity = MacroCalculatorService.calculate_nutrition_for_quantity(
            food_data['nutrition_per_100g'],
            quantity
        )
        
        return Response({
            'food_info': food_data,
            'nutrition_for_quantity': nutrition_for_quantity,
            'quantity_g': quantity
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NutritionLogListCreateView(generics.ListCreateAPIView):
    serializer_class = NutritionLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = NutritionLog.objects.filter(user=self.request.user)
        
        date_filter = self.request.query_params.get('date')
        if date_filter:
            try:
                filter_date = date.fromisoformat(date_filter)
                queryset = queryset.filter(date_eaten__date=filter_date)
            except ValueError:
                pass
        
        return queryset.order_by('-date_eaten')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def daily_nutrition_summary(request):
    """Get daily nutrition summary for the current user"""
    target_date = request.query_params.get('date', date.today())
    if isinstance(target_date, str):
        target_date = date.fromisoformat(target_date)
    
    daily_logs = NutritionLog.objects.filter(
        user=request.user,
        date_eaten__date=target_date
    )
    
    daily_totals = daily_logs.aggregate(
        total_calories=Sum('calories'),
        total_protein=Sum('protein_g'),
        total_carbs=Sum('carbohydrates_g'),
        total_fat=Sum('fat_g'),
        total_fiber=Sum('fiber_g'),
        total_sugar=Sum('sugar_g'),
        total_sodium=Sum('sodium_mg'),
    )
    
    meals = {}
    for meal_type, _ in NutritionLog.MEAL_TYPE_CHOICES:
        meal_logs = daily_logs.filter(meal_type=meal_type)
        meals[meal_type] = {
            'logs': NutritionLogSerializer(meal_logs, many=True).data,
            'totals': meal_logs.aggregate(
                calories=Sum('calories'),
                protein=Sum('protein_g'),
                carbs=Sum('carbohydrates_g'),
                fat=Sum('fat_g'),
            )
        }
    tdee = None
    if hasattr(request.user, 'metrics'):
        tdee = request.user.metrics.calculate_tdee()
    
    return Response({
        'date': target_date,
        'daily_totals': daily_totals,
        'meals': meals,
        'tdee': tdee,
        'calories_remaining': tdee - (daily_totals.get('total_calories') or 0) if tdee else None
    })
