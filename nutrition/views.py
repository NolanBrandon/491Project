from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum, Count, Avg
from django.utils.dateparse import parse_date
from datetime import date, timedelta, datetime
from decimal import Decimal

from .models import NutritionLog
from .serializers import (
    NutritionLogSerializer, 
    BarcodeSearchSerializer,
    BarcodeSearchResponseSerializer,
    CreateNutritionLogFromBarcodeSerializer
)
from .services import OpenFoodFactsService, MacroCalculatorService


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def scan_barcode(request):
    serializer = BarcodeSearchSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    barcode = serializer.validated_data['barcode']
    quantity = serializer.validated_data['quantity']

    try:
        cached_food = FoodDatabase.objects.get(barcode=barcode)
        food_data = {
            'barcode': cached_food.barcode,
            'name': cached_food.name,
            'brand': cached_food.brand or '',
            'nutrition_per_100g': {
                'calories': float(cached_food.calories_per_100g),
                'protein': float(cached_food.protein_per_100g),
                'carbohydrates': float(cached_food.carbs_per_100g),
                'fat': float(cached_food.fat_per_100g),
                'fiber': float(cached_food.fiber_per_100g),
                'sugar': float(cached_food.sugar_per_100g),
                'sodium': float(cached_food.sodium_per_100g),
            }
        }
    except FoodDatabase.DoesNotExist:
       
        food_data = OpenFoodFactsService.get_product_by_barcode(barcode)
    
    if 'error' in food_data:
        return Response(
            {'error': food_data['error']}, 
            status=status.HTTP_404_NOT_FOUND
        )

    FoodDatabase.objects.create(
            barcode=barcode,
            name=food_data['name'],
            brand=food_data.get('brand', ''),
            calories_per_100g=food_data['nutrition_per_100g']['calories'],
            protein_per_100g=food_data['nutrition_per_100g']['protein'],
            carbs_per_100g=food_data['nutrition_per_100g']['carbohydrates'],
            fat_per_100g=food_data['nutrition_per_100g']['fat'],
            fiber_per_100g=food_data['nutrition_per_100g'].get('fiber', 0),
            sugar_per_100g=food_data['nutrition_per_100g'].get('sugar', 0),
            sodium_per_100g=food_data['nutrition_per_100g'].get('sodium', 0),
        )
    
    nutrition_for_quantity = MacroCalculatorService.calculate_nutrition_for_quantity(
        food_data['nutrition_per_100g'],
        float(quantity)
    )
    
    return Response({
        'barcode': food_data['barcode'],
        'name': food_data['name'],
        'brand': food_data['brand', ' '],
        'quantity_g': float(quantity),
        'nutrition_per_100g': food_data['nutrition_per_100g'],
        'nutrition_total': nutrition_for_quantity
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def log_from_barcode(request):
  
    serializer = CreateNutritionLogFromBarcodeSerializer(
        data=request.data,
        context={'request': request}
    )
    
    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        log = serializer.save()
        response_serializer = NutritionLogSerializer(log)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )
    except Exception as e:
        return Response(
            {'error': f'Failed to create log: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class NutritionLogListCreateView(generics.ListCreateAPIView):
    serializer_class = NutritionLogSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = NutritionLog.objects.filter(user=self.request.user)
        
        date_filter = self.request.query_params.get('date')
        if date_filter:
            parsed_date = parse_date(date_filter)
            if parsed_date:
                queryset = queryset.filter(date_eaten__date=parsed_date)
        
        meal_type = self.request.query_params.get('meal_type')
        if meal_type:
            queryset = queryset.filter(meal_type=meal_type)
        
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date:
            parsed_start = parse_date(start_date)
            if parsed_start:
                queryset = queryset.filter(date_eaten__date__gte=parsed_start)
        
        if end_date:
            parsed_end = parse_date(end_date)
            if parsed_end:
                queryset = queryset.filter(date_eaten__date__lte=parsed_end)
        
        return queryset.order_by('-date_eaten')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class NutritionLogDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NutritionLogSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return NutritionLog.objects.filter(user=self.request.user)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def daily_nutrition_summary(request):
    date_param = request.query_params.get('date')
    if date_param:
        target_date = parse_date(date_param)
        if not target_date:
            return Response(
                {'error': 'Invalid date format. Use YYYY-MM-DD'},
                status=status.HTTP_400_BAD_REQUEST
            )
    else:
        target_date = date.today()
    
    daily_logs = NutritionLog.objects.filter(
        user=request.user,
        date_eaten__date=target_date
    )

    from django.db.models.functions import Coalesce
    
    daily_totals = daily_logs.aggregate(
        total_calories=Coalesce(Sum('calories'), 0),
        total_protein=Coalesce(Sum('protein_g'), 0),  
        total_carbs=Coalesce(Sum('carbohydrates_g'), 0),  
        total_fat=Coalesce(Sum('fat_g'), 0),  
        total_fiber=Coalesce(Sum('fiber_g'), 0),  
        total_sugar=Coalesce(Sum('sugar_g'), 0),  
        total_sodium=Coalesce(Sum('sodium_mg'), 0), 
    )

    meals = {}
    for meal_type, meal_label in NutritionLog.MEAL_TYPE_CHOICES:  # Fixed tuple unpacking
        meal_logs = daily_logs.filter(meal_type=meal_type)
        meals[meal_type] = {
            'logs': NutritionLogSerializer(meal_logs, many=True).data,
            'totals': meal_logs.aggregate(
                calories=Coalesce(Sum('calories'), 0),
                protein=Coalesce(Sum('protein_g'), 0),  # Fixed
                carbs=Coalesce(Sum('carbohydrates_g'), 0),  # Fixed
                fat=Coalesce(Sum('fat_g'), 0),  # Fixed
            )
        }
    
tdee = None
    calories_remaining = None
    if hasattr(request.user, 'metrics'):
        try:
            tdee = request.user.metrics.calculate_tdee()
            if tdee:
                calories_remaining = tdee - (daily_totals['total_calories'] or 0)
        except (AttributeError, Exception):
            pass
    
    return Response({
        'date': target_date,
        'daily_totals': daily_totals,
        'meals': meals,
        'tdee': tdee,
        'calories_remaining': calories_remaining
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def weekly_nutrition_summary(request):
   
    start_date_param = request.query_params.get('start_date')
    
    if start_date_param:
        start_date = parse_date(start_date_param)
        if not start_date:
            return Response(
                {'error': 'Invalid date format. Use YYYY-MM-DD'},
                status=status.HTTP_400_BAD_REQUEST
            )
    else:
        today = date.today()
        start_date = today - timedelta(days=today.weekday())  # Monday
    
    end_date = start_date + timedelta(days=6)  # Sunday

    weekly_logs = NutritionLog.objects.filter(
        user=request.user,
        date_eaten__date__gte=start_date,
        date_eaten__date__lte=end_date
    )
    
    # Calculate weekly totals
    weekly_totals = weekly_logs.aggregate(
        total_calories=Sum('calories'),
        total_protein=Sum('protein_g'),
        total_carbs=Sum('carbohydrates_g'),
        total_fat=Sum('fat_g'),
        avg_daily_calories=Avg('calories'),
        meal_count=Count('id')
    )
    
    # Daily breakdown
    daily_breakdown = []
    current_date = start_date
    
    while current_date <= end_date:
        day_logs = weekly_logs.filter(date_eaten__date=current_date)
        day_totals = day_logs.aggregate(
            calories=Sum('calories'),
            protein=Sum('protein_g'),
            carbs=Sum('carbohydrates_g'),
            fat=Sum('fat_g'),
        )
        
        daily_breakdown.append({
            'date': current_date,
            'day_name': current_date.strftime('%A'),
            'totals': day_totals,
            'meal_count': day_logs.count()
        })
        
        current_date += timedelta(days=1)
    
    return Response({
        'start_date': start_date,
        'end_date': end_date,
        'weekly_totals': weekly_totals,
        'daily_breakdown': daily_breakdown
    })


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_meal(request):
    target_date = request.query_params.get('date')
    meal_type = request.query_params.get('meal_type')
    
    if not target_date or not meal_type:
        return Response(
            {'error': 'Both date and meal_type are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    parsed_date = parse_date(target_date)
    if not parsed_date:
        return Response(
            {'error': 'Invalid date format. Use YYYY-MM-DD'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    deleted_count, _ = NutritionLog.objects.filter(
        user=request.user,
        date_eaten__date=parsed_date,
        meal_type=meal_type
    ).delete()
    
    return Response({
        'message': f'Deleted {deleted_count} log(s)',
        'deleted_count': deleted_count
    }, status=status.HTTP_200_OK)
