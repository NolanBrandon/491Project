import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from decouple import config
import logging
import json

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
            genai.configure(api_key=self.api_key)
            self.model_id = "gemini-2.5-flash"
            
            # Configure safety settings to be less restrictive for food content
            safety_settings = {
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }
            
            self.model = genai.GenerativeModel(
                self.model_id,
                safety_settings=safety_settings
            )
            logger.info("Gemini AI service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini AI service: {e}")
            raise

    def test_connection(self):
        """Test the AI connection with a simple query."""
        try:
            response = self.model.generate_content("Hello, are you working?")
            return True, response.text
        except Exception as e:
            logger.error(f"AI connection test failed: {e}")
            return False, str(e)

    def generate_exercise_plan(self, user_goal: str, experience_level: str, days_per_week: int, user_profile: dict):
        """
        Generate a personalized exercise plan using Gemini AI.
        
        Args:
            user_goal (str): The user's primary fitness goal (e.g., "build muscle", "lose weight")
            experience_level (str): The user's workout experience (e.g., "beginner", "intermediate")
            days_per_week (int): The number of days the user can work out
            user_profile (dict): A dictionary with user's metrics (e.g., age, gender)
                
        Returns:
            dict: Structured exercise plan response
        """
        try:
            prompt = self._create_workout_plan_prompt(user_goal, experience_level, days_per_week, user_profile)
            
            # Configure generation with extended timeout
            generation_config = genai.GenerationConfig(
                response_mime_type="application/json",
                max_output_tokens=16384,  # Increased token limit for detailed workout plans
                temperature=0.7
            )
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config,
                request_options={'timeout': 180}  # 3 minutes timeout
            )
            
            logger.info("Exercise plan generated successfully")
            return self._parse_json_response(response.text, "exercise_plan")
            
        except Exception as e:
            logger.error(f"Error generating exercise plan: {e}")
            raise

    def generate_meal_plan(self, user_goal: str, daily_calorie_target: int, dietary_preferences: list, user_profile: dict):
        """
        Generate a personalized meal plan using Gemini AI.
        
        Args:
            user_goal (str): The user's primary fitness goal (e.g., "build muscle", "lose weight")
            daily_calorie_target (int): The user's target daily calorie intake
            dietary_preferences (list): A list of dietary restrictions or preferences
            user_profile (dict): A dictionary with user's metrics (e.g., age, gender)
                
        Returns:
            dict: Structured meal plan response
        """
        try:
            prompt = self._create_meal_plan_prompt(user_goal, daily_calorie_target, dietary_preferences, user_profile)
            
            # Configure generation with extended timeout and higher token limit
            generation_config = genai.GenerationConfig(
                response_mime_type="application/json",
                max_output_tokens=32768,  # Significantly increased for very detailed meal plans
                temperature=0.7
            )
            
            # Use streaming or configure client timeout
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config,
                request_options={'timeout': 180}  # 3 minutes timeout
            )
            
            logger.info("Meal plan generated successfully")
            
            # Check if response was blocked by safety filters
            if not response.candidates:
                logger.error("No candidates returned - response may have been blocked")
                return {"success": False, "error": "Response was blocked by safety filters"}
            
            candidate = response.candidates[0]
            if candidate.finish_reason.name == "SAFETY":
                safety_ratings = {rating.category.name: rating.probability.name for rating in candidate.safety_ratings}
                logger.error(f"Response blocked by safety filters: {safety_ratings}")
                return {"success": False, "error": f"Response blocked by safety filters: {safety_ratings}"}
            
            if not response.text:
                logger.error("Empty response text")
                return {"success": False, "error": "Empty response from AI service"}
            
            return self._parse_json_response(response.text, "meal_plan")
            
        except Exception as e:
            logger.error(f"Error generating meal plan: {e}")
            raise

    def _create_workout_plan_prompt(self, user_goal: str, experience_level: str, days_per_week: int, user_profile: dict) -> str:
        """
        Generates a detailed prompt for the Gemini API to create a personalized workout plan.

        Args:
            user_goal: The user's primary fitness goal (e.g., "build muscle", "lose weight").
            experience_level: The user's workout experience (e.g., "beginner", "intermediate").
            days_per_week: The number of days the user can work out.
            user_profile: A dictionary with user's metrics (e.g., age, gender).

        Returns:
            A formatted string to be used as a prompt for the Gemini API.
        """
        
        # This is the example JSON structure you want the AI to follow.
        json_structure_example = {
          "plan_name": "4-Day Muscle Building Split",
          "plan_description": "A 4-day split designed to maximize muscle growth by targeting major muscle groups.",
          "days": [
            {
              "day_number": 1,
              "day_name": "Upper Body Strength",
              "exercises": [
                {
                  "exercise_name": "Bench Press",
                  "sets": 4,
                  "reps": "6-8"
                },
                {
                  "exercise_name": "Bent Over Row",
                  "sets": 4,
                  "reps": "6-8"
                }
              ]
            }
          ]
        }

        prompt = f"""
        You are an expert fitness coach and personal trainer. Your task is to create a personalized, {days_per_week}-day workout plan based on the user's profile and goals.

        **User Profile:**
        - Goal: {user_goal}
        - Experience Level: {experience_level}
        - Age: {user_profile.get('age')}
        - Gender: {user_profile.get('gender')}
        
        **Instructions:**
        1. Create a logical weekly split appropriate for the user's goal and available days.
        2. Select exercises that are effective and safe for the user's experience level.
        3. Provide a clear number of sets and a target repetition range for each exercise.

        **Output Format:**
        You MUST format your response as a single, valid JSON object. Do not include any introductory text, explanations, or markdown formatting like ```json. Your entire response must be the JSON object itself, matching this exact structure:

        {json.dumps(json_structure_example, indent=2)}
        """
        
        return prompt.strip()

    def _create_meal_plan_prompt(self, user_goal: str, daily_calorie_target: int, dietary_preferences: list, user_profile: dict) -> str:
        """
        Generates a detailed prompt for the Gemini API to create a personalized meal plan.

        Args:
            user_goal: The user's primary fitness goal (e.g., "build muscle", "lose weight").
            daily_calorie_target: The user's target daily calorie intake.
            dietary_preferences: A list of dietary restrictions or preferences (e.g., ["vegetarian", "no nuts"]).
            user_profile: A dictionary with user's metrics (e.g., age, gender).

        Returns:
            A formatted string to be used as a prompt for the Gemini API.
        """

        # This is the example JSON structure you want the AI to follow.
        json_structure_example = {
          "plan_name": "5-Day High-Protein Meal Plan",
          "plan_description": "A 5-day meal plan focused on high-protein sources to support muscle repair and growth.",
          "days": [
            {
              "day_number": 1,
              "meals": {
                "breakfast": {
                  "recipe_name": "Scrambled Eggs with Spinach and Feta",
                  "ingredients": [
                    {
                      "ingredient_name": "Eggs",
                      "measure": "3 large",
                      "calories": 210,
                      "protein": 18,
                      "carbs": 1,
                      "fat": 15,
                      "trans_fat": 0,
                      "fiber": 0,
                      "sugar": 1
                    },
                    {
                      "ingredient_name": "Spinach",
                      "measure": "1 cup",
                      "calories": 7,
                      "protein": 1,
                      "carbs": 1,
                      "fat": 0,
                      "trans_fat": 0,
                      "fiber": 1,
                      "sugar": 0
                    },
                    {
                      "ingredient_name": "Feta Cheese",
                      "measure": "2 oz",
                      "calories": 150,
                      "protein": 8,
                      "carbs": 2,
                      "fat": 12,
                      "trans_fat": 0,
                      "fiber": 0,
                      "sugar": 2
                    }
                  ],
                  "meal_totals": {
                    "calories": 367,
                    "protein": 27,
                    "carbs": 4,
                    "fat": 27,
                    "trans_fat": 0,
                    "fiber": 1,
                    "sugar": 3
                  },
                  "prep_time": 10,
                  "instructions": "Heat pan over medium heat, scramble eggs with spinach, top with crumbled feta"
                },
                "lunch": {
                  "recipe_name": "Grilled Chicken Salad with Vinaigrette",
                  "ingredients": [
                    {
                      "ingredient_name": "Chicken Breast",
                      "measure": "6 oz",
                      "calories": 280,
                      "protein": 53,
                      "carbs": 0,
                      "fat": 6,
                      "trans_fat": 0,
                      "fiber": 0,
                      "sugar": 0
                    },
                    {
                      "ingredient_name": "Mixed Greens",
                      "measure": "3 cups",
                      "calories": 20,
                      "protein": 2,
                      "carbs": 4,
                      "fat": 0,
                      "trans_fat": 0,
                      "fiber": 2,
                      "sugar": 2
                    }
                  ],
                  "meal_totals": {
                    "calories": 300,
                    "protein": 55,
                    "carbs": 4,
                    "fat": 6,
                    "trans_fat": 0,
                    "fiber": 2,
                    "sugar": 2
                  },
                  "prep_time": 15,
                  "instructions": "Grill chicken breast, serve over mixed greens with vinaigrette"
                },
                "dinner": {
                  "recipe_name": "Baked Salmon with Quinoa",
                  "ingredients": [
                    {
                      "ingredient_name": "Salmon Fillet",
                      "measure": "5 oz",
                      "calories": 350,
                      "protein": 40,
                      "carbs": 0,
                      "fat": 20,
                      "trans_fat": 0,
                      "fiber": 0,
                      "sugar": 0
                    }
                  ],
                  "meal_totals": {
                    "calories": 350,
                    "protein": 40,
                    "carbs": 0,
                    "fat": 20,
                    "trans_fat": 0,
                    "fiber": 0,
                    "sugar": 0
                  },
                  "prep_time": 20,
                  "instructions": "Bake salmon at 400°F for 15 minutes"
                }
              },
              "daily_totals": {
                "calories": 1017,
                "protein": 122,
                "carbs": 8,
                "fat": 53,
                "trans_fat": 0,
                "fiber": 3,
                "sugar": 5
              }
            }
          ]
        }
        
        prompt = f"""
        You are an expert nutritionist and meal planner. Your task is to create a personalized 5-day meal plan based on the user's profile, goals, and dietary needs.

        **User Profile:**
        - Goal: {user_goal}
        - Target Daily Calories: Approximately {daily_calorie_target} kcal
        - Dietary Preferences/Restrictions: {', '.join(dietary_preferences) if dietary_preferences else 'None'}
        - Age: {user_profile.get('age')}
        - Gender: {user_profile.get('gender')}

        **Instructions:**
        1. Generate creative and healthy recipes for breakfast, lunch, and dinner for 5 days.
        2. For each recipe, list the primary ingredients with their measurements and complete nutritional breakdown.
        3. Calculate accurate meal totals by summing all ingredient macros.
        4. Provide daily totals by summing all meals for each day.
        5. Ensure the overall plan aligns with the user's calorie target and dietary preferences.
        6. Include realistic prep times and clear cooking instructions.

        **Nutritional Requirements:**
        - Provide calories, protein, carbs, fat, trans_fat, fiber, and sugar for each ingredient
        - Calculate meal_totals for each meal (sum of all ingredients)
        - Calculate daily_totals for each day (sum of all meals)
        - Use realistic nutritional values based on standard food databases

        **Output Format:**
        You MUST format your response as a single, valid JSON object. Do not include any introductory text, explanations, or markdown formatting like ```json. Your entire response must be the JSON object itself, matching this exact structure:

        {json.dumps(json_structure_example, indent=2)}
        """
        
        return prompt.strip()

    def _parse_json_response(self, response_text, expected_type):
        """Parse JSON response from AI and handle errors gracefully."""
        try:
            # Clean up the response text
            response_text = response_text.strip()
            
            # If response is truncated, try to fix common JSON issues
            if not response_text.endswith('}'):
                logger.warning("Response appears truncated, attempting to fix JSON")
                # Count open braces vs close braces
                open_braces = response_text.count('{')
                close_braces = response_text.count('}')
                missing_braces = open_braces - close_braces
                
                # Add missing closing braces
                if missing_braces > 0:
                    response_text += '}' * missing_braces
                    logger.info(f"Added {missing_braces} closing braces to fix JSON")
            
            parsed_data = json.loads(response_text)
            logger.info(f"Successfully parsed {expected_type} response")
            return {"success": True, "data": parsed_data}
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error for {expected_type}: {e}. Raw response: {response_text[:1000]}...")
            
            # Try to extract partial data if possible
            try:
                # Find the first complete object
                start_idx = response_text.find('{')
                if start_idx != -1:
                    # Try to find a reasonable cutoff point
                    for end_idx in range(len(response_text) - 1, start_idx, -1):
                        if response_text[end_idx] == '}':
                            try:
                                partial_response = response_text[start_idx:end_idx + 1]
                                parsed_data = json.loads(partial_response)
                                logger.warning(f"Successfully parsed partial {expected_type} response")
                                return {"success": True, "data": parsed_data, "partial": True}
                            except json.JSONDecodeError:
                                continue
                                
            except Exception as fallback_error:
                logger.error(f"Fallback parsing also failed: {fallback_error}")
            
            return {"success": False, "error": f"Failed to parse AI response as JSON: {str(e)}"}
            
        except Exception as e:
            logger.error(f"Unexpected error parsing {expected_type}: {e}")
            return {"success": False, "error": f"Unexpected error: {str(e)}"}