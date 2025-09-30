import os
import sys
import django
import time
import statistics
from django.test import TestCase
from unittest.mock import patch, MagicMock
from concurrent.futures import ThreadPoolExecutor

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'easyfitness_backend.settings')
django.setup()

from api.services import GeminiAIService


class AIServicePerformanceTests(TestCase):
    """Performance tests for GeminiAIService - measuring response times."""
    
    @patch('api.services.ai_service.config')
    @patch('api.services.ai_service.genai.configure')
    @patch('api.services.ai_service.genai.GenerativeModel')
    def test_exercise_plan_generation_timeout(self, mock_model, mock_configure, mock_config):
        """Ensure exercise plan generation completes within 30 seconds (AI API timeout)."""
        mock_config.return_value = "fake-api-key"
      
        def slow_generate(*args, **kwargs):
            time.sleep(0.5)  # Simulate network delay
            response = MagicMock()
            response.text = '{"plan_name": "Test", "plan_description": "Test", "days": []}'
            return response
        
        mock_instance = MagicMock()
        mock_instance.generate_content = slow_generate
        mock_model.return_value = mock_instance
        
        ai_service = GeminiAIService()
        
        start = time.time()
        result = ai_service.generate_exercise_plan(
            "build muscle", "beginner", 3, {"age": 25, "gender": "male"}
        )
        duration = time.time() - start
        
        self.assertTrue(result['success'])
        self.assertLess(
            duration, 30.0,
            f"Exercise plan generation took {duration:.2f}s (timeout threshold: 30s)"
        )
        print(f"✅ Exercise plan generation completed in {duration:.3f}s")
    
    @patch('api.services.ai_service.config')
    @patch('api.services.ai_service.genai.configure')
    @patch('api.services.ai_service.genai.GenerativeModel')
    def test_meal_plan_generation_timeout(self, mock_model, mock_configure, mock_config):
        """Ensure meal plan generation completes within 30 seconds (AI API timeout)."""
        mock_config.return_value = "fake-api-key"
        
        def slow_generate(*args, **kwargs):
            time.sleep(0.5)
            response = MagicMock()
            response.text = '{"plan_name": "Test", "plan_description": "Test", "days": []}'
            return response
        
        mock_instance = MagicMock()
        mock_instance.generate_content = slow_generate
        mock_model.return_value = mock_instance
        
        ai_service = GeminiAIService()
        
        start = time.time()
        result = ai_service.generate_meal_plan(
            "lose weight", 1800, ["vegetarian"], {"age": 30, "gender": "female"}
        )
        duration = time.time() - start
        
        self.assertTrue(result['success'])
        self.assertLess(
            duration, 30.0,
            f"Meal plan generation took {duration:.2f}s (timeout threshold: 30s)"
        )
        print(f"✅ Meal plan generation completed in {duration:.3f}s")
    
    @patch('api.services.ai_service.config')
    @patch('api.services.ai_service.genai.configure')
    @patch('api.services.ai_service.genai.GenerativeModel')
    def test_concurrent_plan_generation(self, mock_model, mock_configure, mock_config):
        """Test that multiple concurrent plan generations don't block each other."""
        mock_config.return_value = "fake-api-key"
        
        def mock_generate(*args, **kwargs):
            time.sleep(0.2)  # Simulate API latency
            response = MagicMock()
            response.text = '{"plan_name": "Test", "plan_description": "Test", "days": []}'
            return response
        
        mock_instance = MagicMock()
        mock_instance.generate_content = mock_generate
        mock_model.return_value = mock_instance
        
        ai_service = GeminiAIService()
        
        def generate_plan(user_id):
            start = time.time()
            result = ai_service.generate_exercise_plan(
                "build muscle", "beginner", 3, {"age": 25, "gender": "male"}
            )
            return time.time() - start, result['success']
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            results = list(executor.map(generate_plan, range(5)))
        
        durations = [r[0] for r in results]
        successes = [r[1] for r in results]
        
        self.assertTrue(all(successes), "Some concurrent requests failed")
        
        avg_duration = statistics.mean(durations)
        max_duration = max(durations)
        
        print(f"✅ Concurrent requests: avg={avg_duration:.3f}s, max={max_duration:.3f}s")
        self.assertLess(max_duration, 1.0, "Concurrent requests are blocking each other")
