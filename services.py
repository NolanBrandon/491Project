import requests
from decimal import Decimal
from .models import FoodDatabase

class OpenFoodFactsService:
    BASE_URL = "https://world.openfoodfacts.org/api/v0/product"
    
    @staticmethod
    def get_product_by_barcode(barcode):
        """Fetch product data from Open Food Facts API"""
        try:
            # First check if we have it cached
            cached_food = FoodDatabase.objects.filter(barcode=barcode).first()
            if cached_food:
                return OpenFoodFactsService._format_cached_response(cached_food)
            
            # Fetch from API
            url = f"{OpenFoodFactsService.BASE_URL}/{barcode}.json"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 1:  # Product found
                    product = data.get('product', {})
                    return OpenFoodFactsService._process_api_response(product, barcode)
            
            return {'error': 'Product not found'}
            
        except requests.RequestException as e:
            return {'error': f'API request failed: {str(e)}'}
        except Exception as e:
            return {'error': f'Unexpected error: {str(e)}'}
    
    @staticmethod
    def _process_api_response(product, barcode):
        """Process API response and cache the result"""
        nutriments = product.get('nutriments', {})
        
        # Extract nutritional data (per 100g)
        nutrition_data = {
            'barcode': barcode,
            'name': product.get('product_name', 'Unknown Product'),
            'brand': product.get('brands', ''),
            'calories_per_100g': Decimal(str(nutriments.get('energy-kcal_100g', 0))),
            'protein_per_100g': Decimal(str(nutriments.get('proteins_100g', 0))),
            'carbs_per_100g': Decimal(str(nutriments.get('carbohydrates_100g', 0))),
            'fat_per_100g': Decimal(str(nutriments.get('fat_100g', 0))),
            'fiber_per_100g': Decimal(str(nutriments.get('fiber_100g', 0))),
            'sugar_per_100g': Decimal(str(nutriments.get('sugars_100g', 0))),
            'sodium_per_100g': Decimal(str(nutriments.get('sodium_100g', 0))),
        }
        
        # Cache the result
        cached_food, created = FoodDatabase.objects.get_or_create(
            barcode=barcode,
            defaults=nutrition_data
        )
        
        return OpenFoodFactsService._format_cached_response(cached_food)
    
    @staticmethod
    def _format_cached_response(cached_food):
        """Format cached food data for API response"""
        return {
            'barcode': cached_food.barcode,
            'name': cached_food.name,
            'brand': cached_food.brand,
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

class MacroCalculatorService:
    @staticmethod
    def calculate_nutrition_for_quantity(nutrition_per_100g, quantity_g):
        """Calculate nutrition values for a specific quantity"""
        multiplier = Decimal(str(quantity_g)) / Decimal('100')
        
        return {
            'calories': nutrition_per_100g['calories'] * multiplier,
            'protein': nutrition_per_100g['protein'] * multiplier,
            'carbohydrates': nutrition_per_100g['carbohydrates'] * multiplier,
            'fat': nutrition_per_100g['fat'] * multiplier,
            'fiber': nutrition_per_100g['fiber'] * multiplier,
            'sugar': nutrition_per_100g['sugar'] * multiplier,
            'sodium': nutrition_per_100g['sodium'] * multiplier,
        }
