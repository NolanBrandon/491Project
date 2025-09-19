from google import genai
from decouple import config
import logging

logger = logging.getLogger(__name__)


class GeminiAIService:
    """
    Service class for integrating with Google's Gemini AI API.
    Handles exercise and meal plan generation using AI.
    """
    
    def __init__(self):
        """Initialize the Gemini AI client with API key from environment."""
        try:
            self.api_key = config('GEMINI_API_KEY')
            self.client = genai.Client(api_key=self.api_key)
            self.model_id = "gemini-2.5-flash"  # Using the same model as in ai_test.py
            logger.info("Gemini AI service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini AI service: {e}")
            raise

    def test_connection(self):
        """Test the AI connection with a simple query."""
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents="Hello, are you working?"
            )
            return True, response.text
        except Exception as e:
            logger.error(f"AI connection test failed: {e}")
            return False, str(e)