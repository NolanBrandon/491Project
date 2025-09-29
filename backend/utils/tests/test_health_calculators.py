from decimal import Decimal
import pytest
from ..health_calculators import HealthCalculators


class TestBMRCalculator:    
    def test_bmr_male_standard(self):
        bmr = HealthCalculators.calculate_bmr(
            weight_kg=80,
            height_cm=180,
            age=30,
            gender='male'
        )
        assert bmr == Decimal('1780.00')
    
    def test_bmr_female_standard(self):
        bmr = HealthCalculators.calculate_bmr(
            weight_kg=65,
            height_cm=165,
            age=28,
            gender='female'
        )
        assert bmr == Decimal('1380.25')
    
    def test_bmr_male_elderly(self):
        bmr = HealthCalculators.calculate_bmr(
            weight_kg=75,
            height_cm=175,
            age=70,
            gender='male'
        )
        assert bmr == Decimal('1498.75')
    
    def test_bmr_female_young(self):
        bmr = HealthCalculators.calculate_bmr(
            weight_kg=55,
            height_cm=160,
            age=20,
            gender='female'
        )
        assert bmr == Decimal('1289.00')
    
    def test_bmr_invalid_weight(self):
        with pytest.raises(ValueError, match="Weight must be positive"):
            HealthCalculators.calculate_bmr(
                weight_kg=-10,
                height_cm=170,
                age=25,
                gender='male'
            )
    
    def test_bmr_zero_weight(self):
        with pytest.raises(ValueError, match="Weight must be positive"):
            HealthCalculators.calculate_bmr(
                weight_kg=0,
                height_cm=170,
                age=25,
                gender='male'
            )
    
    def test_bmr_invalid_height(self):
        with pytest.raises(ValueError, match="Height must be positive"):
            HealthCalculators.calculate_bmr(
                weight_kg=70,
                height_cm=-180,
                age=25,
                gender='male'
            )
    
    def test_bmr_invalid_age(self):
        with pytest.raises(ValueError, match="Age must be positive"):
            HealthCalculators.calculate_bmr(
                weight_kg=70,
                height_cm=180,
                age=-5,
                gender='male'
            )
    
    def test_bmr_invalid_gender(self):
        with pytest.raises(ValueError, match="Gender must be 'male' or 'female'"):
            HealthCalculators.calculate_bmr(
                weight_kg=70,
                height_cm=180,
                age=25,
                gender='other'
            )
    
    def test_bmr_precision(self):
        bmr = HealthCalculators.calculate_bmr(
            weight_kg=70.5,
            height_cm=175.5,
            age=25,
            gender='male'
        )
        assert isinstance(bmr, Decimal)
        assert str(bmr).split('.')[1] == '63' if '.' in str(bmr) else True


class TestTDEECalculator:
    def test_tdee_sedentary(self):
        bmr = 1800
        tdee = HealthCalculators.calculate_tdee(bmr, 'sedentary')
        assert tdee == Decimal('2160.00')
    
    def test_tdee_lightly_active(self):
        bmr = 1800
        tdee = HealthCalculators.calculate_tdee(bmr, 'lightly_active')
        assert tdee == Decimal('2475.00')
    
    def test_tdee_moderately_active(self):
        bmr = 1800
        tdee = HealthCalculators.calculate_tdee(bmr, 'moderately_active')
        assert tdee == Decimal('2790.00')
    
    def test_tdee_very_active(self):
        bmr = 1800
        tdee = HealthCalculators.calculate_tdee(bmr, 'very_active')
        assert tdee == Decimal('3105.00')
    
    def test_tdee_extremely_active(self):
        bmr = 1800
        tdee = HealthCalculators.calculate_tdee(bmr, 'extremely_active')
        # Expected: 1800 * 1.9 = 3420
        assert tdee == Decimal('3420.00')
    
    def test_tdee_invalid_activity_level(self):
        with pytest.raises(ValueError, match="Invalid activity level"):
            HealthCalculators.calculate_tdee(1800, 'super_active')
    
    def test_tdee_with_decimal_bmr(self):
        bmr = 1785.50
        tdee = HealthCalculators.calculate_tdee(bmr, 'moderately_active')
        # Expected: 1785.50 * 1.55 = 2767.525 ≈ 2767.53
        assert tdee == Decimal('2767.53')


class TestRMRCalculator:
    def test_rmr_male(self):
        rmr = HealthCalculators.calculate_rmr(
            weight_kg=80,
            height_cm=180,
            age=30,
            gender='male'
        )
        bmr = HealthCalculators.calculate_bmr(80, 180, 30, 'male')
        expected_rmr = bmr * Decimal('1.1')
        assert rmr == expected_rmr.quantize(Decimal('0.01'))
    
    def test_rmr_female(self):
        rmr = HealthCalculators.calculate_rmr(
            weight_kg=65,
            height_cm=165,
            age=28,
            gender='female'
        )
        bmr = HealthCalculators.calculate_bmr(65, 165, 28, 'female')
        expected_rmr = bmr * Decimal('1.1')
        assert rmr == expected_rmr.quantize(Decimal('0.01'))
    
    def test_rmr_invalid_inputs(self):
        with pytest.raises(ValueError):
            HealthCalculators.calculate_rmr(-50, 170, 25, 'male')


class TestMETCalculator:
    def test_met_moderate_effort(self):
        calories = HealthCalculators.calculate_calories_burned_met(
            met_value=8.0,  # Running at 8 km/h
            weight_kg=70,
            duration_minutes=30,
            perceived_effort='moderate'
        )
        assert calories == Decimal('280.00')
    
    def test_met_low_effort(self):
        calories = HealthCalculators.calculate_calories_burned_met(
            met_value=6.0,
            weight_kg=70,
            duration_minutes=60,
            perceived_effort='low'
        )
        assert calories == Decimal('357.00')
    
    def test_met_high_effort(self):
        calories = HealthCalculators.calculate_calories_burned_met(
            met_value=10.0,
            weight_kg=70,
            duration_minutes=45,
            perceived_effort='high'
        )
        assert calories == Decimal('603.75')
    
    def test_met_different_weight(self):
        calories_light = HealthCalculators.calculate_calories_burned_met(
            met_value=5.0,
            weight_kg=60,
            duration_minutes=30,
            perceived_effort='moderate'
        )
        calories_heavy = HealthCalculators.calculate_calories_burned_met(
            met_value=5.0,
            weight_kg=90,
            duration_minutes=30,
            perceived_effort='moderate'
        )
        assert calories_heavy > calories_light
        
        ratio = calories_heavy / calories_light
        assert ratio == Decimal('1.5')
    
    def test_met_invalid_met_value(self):
        with pytest.raises(ValueError, match="MET value must be positive"):
            HealthCalculators.calculate_calories_burned_met(-5, 70, 30)
    
    def test_met_invalid_weight(self):
        with pytest.raises(ValueError, match="Weight must be positive"):
            HealthCalculators.calculate_calories_burned_met(5, -70, 30)
    
    def test_met_invalid_duration(self):
        with pytest.raises(ValueError, match="Duration must be positive"):
            HealthCalculators.calculate_calories_burned_met(5, 70, -30)
    
    def test_met_invalid_effort(self):
        with pytest.raises(ValueError, match="Perceived effort must be"):
            HealthCalculators.calculate_calories_burned_met(
                5, 70, 30, perceived_effort='extreme'
            )
    
    def test_met_precision(self):
        calories = HealthCalculators.calculate_calories_burned_met(
            met_value=7.5,
            weight_kg=72.5,
            duration_minutes=37,
            perceived_effort='moderate'
        )
        assert isinstance(calories, Decimal)
        assert len(str(calories).split('.')[1]) == 2


class TestIntegratedScenarios:
    
    def test_weight_loss_scenario(self):
        bmr = HealthCalculators.calculate_bmr(75, 165, 30, 'female')
        tdee = HealthCalculators.calculate_tdee(bmr, 'sedentary')
        
        recommended_calories = tdee - Decimal('500')  
        
        assert bmr > Decimal('1400')  # Reasonable BMR
        assert tdee > bmr  # TDEE should be higher than BMR
        assert recommended_calories > Decimal('1200')  # Not too low
    
    def test_muscle_gain_scenario(self):
        bmr = HealthCalculators.calculate_bmr(70, 180, 25, 'male')
        tdee = HealthCalculators.calculate_tdee(bmr, 'very_active')

        recommended_calories = tdee + Decimal('300')  
        
        assert tdee > Decimal('2500')  
        assert recommended_calories > tdee
    
    def test_exercise_session_tracking(self):
        """Test tracking a complete exercise session."""
        calories_burned = HealthCalculators.calculate_calories_burned_met(
            met_value=7.0,
            weight_kg=70,
            duration_minutes=45,
            perceived_effort='moderate'
        )
        
        # Should burn reasonable amount
        assert Decimal('300') < calories_burned < Decimal('450')


# Pytest configuration
@pytest.fixture
def sample_user_male():
    """Fixture for standard male user data."""
    return {
        'weight_kg': 80,
        'height_cm': 180,
        'age': 30,
        'gender': 'male'
    }


@pytest.fixture
def sample_user_female():
    """Fixture for standard female user data."""
    return {
        'weight_kg': 65,
        'height_cm': 165,
        'age': 28,
        'gender': 'female'
    }
