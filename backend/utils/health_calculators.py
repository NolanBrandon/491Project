from typing import Literal
from decimal import Decimal, ROUND_HALF_UP

class HealthCalculators:
    """
    Calculators for various health and fitness metrics.
    All calculations use the Decimal type for precision.
    """
    
    # Activity level multipliers for TDEE
    ACTIVITY_MULTIPLIERS = {
        'sedentary': Decimal('1.2'),      # Little or no exercise
        'lightly_active': Decimal('1.375'), # Light exercise 1-3 days/week
        'moderately_active': Decimal('1.55'), # Moderate exercise 3-5 days/week
        'very_active': Decimal('1.725'),   # Hard exercise 6-7 days/week
        'extremely_active': Decimal('1.9') # Very hard exercise, physical job
    }
    
    @staticmethod
    def calculate_bmr(
        weight_kg: float,
        height_cm: float,
        age: int,
        gender: Literal['male', 'female']
    ) -> Decimal:
        """
        Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation.
        
        Formula:
        - Men: BMR = 10 × weight(kg) + 6.25 × height(cm) − 5 × age(y) + 5
        - Women: BMR = 10 × weight(kg) + 6.25 × height(cm) − 5 × age(y) − 161
        
        Args:
            weight_kg: Weight in kilograms
            height_cm: Height in centimeters
            age: Age in years
            gender: 'male' or 'female'
            
        Returns:
            BMR in calories per day (Decimal)
            
        Raises:
            ValueError: If inputs are invalid
        """
        # Validate inputs
        if weight_kg <= 0:
            raise ValueError("Weight must be positive")
        if height_cm <= 0:
            raise ValueError("Height must be positive")
        if age <= 0:
            raise ValueError("Age must be positive")
        if gender not in ['male', 'female']:
            raise ValueError("Gender must be 'male' or 'female'")
        
        # Convert to Decimal for precision
        weight = Decimal(str(weight_kg))
        height = Decimal(str(height_cm))
        age_dec = Decimal(str(age))
        
        # Calculate base value
        bmr = (Decimal('10') * weight + 
               Decimal('6.25') * height - 
               Decimal('5') * age_dec)
        
        # Add gender-specific adjustment
        if gender == 'male':
            bmr += Decimal('5')
        else:  # female
            bmr -= Decimal('161')
        
        return bmr.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    @staticmethod
    def calculate_tdee(
        bmr: float,
        activity_level: str
    ) -> Decimal:
        """
        Calculate Total Daily Energy Expenditure.
        
        TDEE = BMR × Activity Multiplier
        
        Args:
            bmr: Basal Metabolic Rate
            activity_level: One of: sedentary, lightly_active, moderately_active,
                           very_active, extremely_active
                           
        Returns:
            TDEE in calories per day (Decimal)
            
        Raises:
            ValueError: If activity level is invalid
        """
        if activity_level not in HealthCalculators.ACTIVITY_MULTIPLIERS:
            raise ValueError(
                f"Invalid activity level. Must be one of: "
                f"{', '.join(HealthCalculators.ACTIVITY_MULTIPLIERS.keys())}"
            )
        
        bmr_dec = Decimal(str(bmr))
        multiplier = HealthCalculators.ACTIVITY_MULTIPLIERS[activity_level]
        
        tdee = bmr_dec * multiplier
        return tdee.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    @staticmethod
    def calculate_rmr(
        weight_kg: float,
        height_cm: float,
        age: int,
        gender: Literal['male', 'female']
    ) -> Decimal:
        """
        Calculate Resting Metabolic Rate.
        
        RMR is similar to BMR but accounts for minimal daily activity.
        This uses a slightly modified approach, typically 10% higher than BMR.
        
        Args:
            weight_kg: Weight in kilograms
            height_cm: Height in centimeters
            age: Age in years
            gender: 'male' or 'female'
            
        Returns:
            RMR in calories per day (Decimal)
        """
        bmr = HealthCalculators.calculate_bmr(weight_kg, height_cm, age, gender)
        rmr = bmr * Decimal('1.1')
        return rmr.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    @staticmethod
    def calculate_calories_burned_met(
        met_value: float,
        weight_kg: float,
        duration_minutes: int,
        perceived_effort: Literal['low', 'moderate', 'high'] = 'moderate'
    ) -> Decimal:
        """
        Calculate calories burned using MET (Metabolic Equivalent of Task).
        
        Formula: Calories = MET × weight(kg) × duration(hours) × effort_multiplier
        
        Effort multipliers adjust for perceived exertion:
        - low: 0.85
        - moderate: 1.0
        - high: 1.15
        
        Args:
            met_value: MET value for the exercise
            weight_kg: Weight in kilograms
            duration_minutes: Duration in minutes
            perceived_effort: Perceived effort level
            
        Returns:
            Calories burned (Decimal)
            
        Raises:
            ValueError: If inputs are invalid
        """
        if met_value <= 0:
            raise ValueError("MET value must be positive")
        if weight_kg <= 0:
            raise ValueError("Weight must be positive")
        if duration_minutes <= 0:
            raise ValueError("Duration must be positive")
        if perceived_effort not in ['low', 'moderate', 'high']:
            raise ValueError("Perceived effort must be 'low', 'moderate', or 'high'")
        
        # Effort multipliers
        effort_multipliers = {
            'low': Decimal('0.85'),
            'moderate': Decimal('1.0'),
            'high': Decimal('1.15')
        }
        
        # Convert to Decimal
        met = Decimal(str(met_value))
        weight = Decimal(str(weight_kg))
        duration_hours = Decimal(str(duration_minutes)) / Decimal('60')
        effort_mult = effort_multipliers[perceived_effort]
        
        # Calculate calories
        calories = met * weight * duration_hours * effort_mult
        return calories.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
