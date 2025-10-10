import requests
from decouple import config
import logging
import json
from typing import Dict, List, Optional, Union
from django.db import transaction

logger = logging.getLogger(__name__)


class ExerciseDBService:
    """
    Service class for integrating with ExerciseDB API.
    Handles exercise data retrieval, search, and integration with AI-generated workout plans. 
    TO DO: AI workout plan enrichment
    """
    
    def __init__(self):
        """Initialize the ExerciseDB API client with API key and base configuration."""
        try:
            self.api_key = config('EXERCISEDB_API_KEY')
            self.base_url = "https://exercisedb-api1.p.rapidapi.com/api/v1"
            self.headers = {
                "x-rapidapi-key": self.api_key,
                "x-rapidapi-host": "exercisedb-api1.p.rapidapi.com"
            }
            logger.info("ExerciseDB service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize ExerciseDB service: {e}")
            raise

    def test_connection(self) -> tuple[bool, str]:
        """
        Test the API connection using the liveness health endpoint. 
        
        API Endpoint: GET /api/v1/liveness
        Response: HTTP 200 status indicates API is alive
        
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            url = f"{self.base_url}/liveness"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                logger.info("ExerciseDB API connection test successful")
                return True, "API connection successful"
            else:
                logger.warning(f"API connection test failed with status: {response.status_code}")
                return False, f"API returned status code: {response.status_code}"
                
        except requests.exceptions.RequestException as e:
            logger.error(f"ExerciseDB API connection test failed: {e}")
            return False, f"Connection error: {str(e)}"
        except Exception as e:
            logger.error(f"Unexpected error during connection test: {e}")
            return False, f"Unexpected error: {str(e)}"

    def get_exercises(self, name: Optional[str] = None, keywords: Optional[str] = None, limit: int = 10) -> Dict:
        """
        Get exercises from the ExerciseDB API with optional filtering.
        
        API Endpoint: GET /api/v1/exercises
        Response Structure:
        {
            "success": true,
            "meta": {
                "total": int,
                "hasNextPage": bool,
                "hasPreviousPage": bool,
                "nextCursor": str
            },
            "data": [
                {
                    "exerciseId": str,
                    "name": str,
                    "imageUrl": str,
                    "bodyParts": [str],
                    "equipments": [str],
                    "exerciseType": str,
                    "targetMuscles": [str],
                    "secondaryMuscles": [str],
                    "keywords": [str]
                }
            ]
        }
        
        Args:
            name (str, optional): Exercise name to search for
            keywords (str, optional): Keywords for filtering exercises
            limit (int): Maximum number of exercises to return (default: 10)
            
        Returns:
            dict: API response containing exercise data
        """
        try:
            url = f"{self.base_url}/exercises"
            querystring = {"limit": str(limit)}
            
            if name:
                querystring["name"] = name
            if keywords:
                querystring["keywords"] = keywords
                
            response = requests.get(url, headers=self.headers, params=querystring, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Successfully retrieved {len(data.get('data', []))} exercises")
                return {
                    "success": True,
                    "data": data,
                    "message": "Exercises retrieved successfully"
                }
            else:
                logger.warning(f"Failed to get exercises. Status: {response.status_code}")
                return {
                    "success": False,
                    "error": f"API returned status code: {response.status_code}",
                    "message": "Failed to retrieve exercises"
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error getting exercises: {e}")
            return {
                "success": False,
                "error": f"Request error: {str(e)}",
                "message": "Failed to connect to ExerciseDB API"
            }
        except Exception as e:
            logger.error(f"Unexpected error getting exercises: {e}")
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "message": "An unexpected error occurred"
            }

    def search_exercises(self, search_term: str) -> Dict:
        """
        Search exercises using the search endpoint.
        
        API Endpoint: GET /api/v1/exercises/search
        Response Structure:
        {
            "success": true,
            "data": [
                {
                    "exerciseId": str,
                    "name": str,
                    "imageUrl": str
                }
            ]
        }
        
        Args:
            search_term (str): Search term for finding exercises
            
        Returns:
            dict: API response containing search results
        """
        try:
            if not search_term:
                return {
                    "success": False,
                    "error": "Search term is required",
                    "message": "Please provide a search term"
                }
                
            url = f"{self.base_url}/exercises/search"
            querystring = {"search": search_term}
            
            response = requests.get(url, headers=self.headers, params=querystring, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Search for '{search_term}' returned {len(data.get('data', []))} results")
                return {
                    "success": True,
                    "data": data,
                    "search_term": search_term,
                    "message": f"Search completed for '{search_term}'"
                }
            else:
                logger.warning(f"Search failed. Status: {response.status_code}")
                return {
                    "success": False,
                    "error": f"API returned status code: {response.status_code}",
                    "message": "Search request failed"
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error during search: {e}")
            return {
                "success": False,
                "error": f"Request error: {str(e)}",
                "message": "Failed to connect to ExerciseDB API"
            }
        except Exception as e:
            logger.error(f"Unexpected error during search: {e}")
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "message": "An unexpected error occurred during search"
            }

    def get_exercise_by_id(self, exercise_id: str) -> Dict:
        """
        Get detailed information about a specific exercise by ID.
        
        API Endpoint: GET /api/v1/exercises/{exercise_id}
        Response Structure:
        {
            "success": true,
            "data": {
                "exerciseId": str,
                "name": str,
                "imageUrl": str,
                "equipments": [str],
                "bodyParts": [str],
                "exerciseType": str,
                "targetMuscles": [str],
                "secondaryMuscles": [str],
                "videoUrl": str,
                "keywords": [str],
                "overview": str,
                "instructions": [str],
                "exerciseTips": [str],
                "variations": [str],
                "relatedExerciseIds": [str]
            }
        }
        
        Args:
            exercise_id (str): The unique ID of the exercise
            
        Returns:
            dict: API response containing exercise details
        """
        try:
            if not exercise_id:
                return {
                    "success": False,
                    "error": "Exercise ID is required",
                    "message": "Please provide a valid exercise ID"
                }
                
            url = f"{self.base_url}/exercises/{exercise_id}"
            
            response = requests.get(url, headers=self.headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Successfully retrieved exercise details for ID: {exercise_id}")
                return {
                    "success": True,
                    "data": data,
                    "exercise_id": exercise_id,
                    "message": "Exercise details retrieved successfully"
                }
            elif response.status_code == 404:
                logger.warning(f"Exercise not found for ID: {exercise_id}")
                return {
                    "success": False,
                    "error": "Exercise not found",
                    "message": f"No exercise found with ID: {exercise_id}"
                }
            else:
                logger.warning(f"Failed to get exercise by ID. Status: {response.status_code}")
                return {
                    "success": False,
                    "error": f"API returned status code: {response.status_code}",
                    "message": "Failed to retrieve exercise details"
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error getting exercise by ID: {e}")
            return {
                "success": False,
                "error": f"Request error: {str(e)}",
                "message": "Failed to connect to ExerciseDB API"
            }
        except Exception as e:
            logger.error(f"Unexpected error getting exercise by ID: {e}")
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "message": "An unexpected error occurred"
            }

    def enrich_workout_plan(self, workout_plan: Dict) -> Dict:
        """
        Enrich an AI-generated workout plan with detailed exercise data from ExerciseDB.
        Also automatically populates the muscles table with any new muscles found.
        
        Args:
            workout_plan (dict): The workout plan from AI service
            
        Returns:
            dict: Enhanced workout plan with exercise details
        """
        try:
            if not workout_plan.get("success", False):
                return {
                    "success": False,
                    "error": "Invalid workout plan provided",
                    "message": "Workout plan must be successful to enrich"
                }
                
            plan_data = workout_plan.get("data", {})
            days = plan_data.get("days", [])
            
            enriched_days = []
            all_muscles_found = set()  # Track all muscles found during enrichment
            all_equipments_found = set()  # Track all equipment found during enrichment
            all_body_parts_found = set()  # Track all body parts found during enrichment
            all_keywords_found = set()  # Track all keywords found during enrichment
            
            for day in days:
                enriched_day = day.copy()
                exercises = day.get("exercises", [])
                enriched_exercises = []
                
                for exercise in exercises:
                    exercise_name = exercise.get("exercise_name", "")
                    
                    # Search for exercise data first
                    search_result = self.search_exercises(exercise_name)
                    
                    enriched_exercise = exercise.copy()
                    
                    if search_result.get("success", False):
                        exercise_data = search_result.get("data", {}).get("data", [])
                        if exercise_data:
                            # Get the exercise ID and fetch detailed data
                            exercise_id = exercise_data[0].get("exerciseId")
                            if exercise_id:
                                # Get detailed exercise information
                                detailed_result = self.get_exercise_by_id(exercise_id)
                                if detailed_result.get("success", False):
                                    detailed_data = detailed_result.get("data", {}).get("data", detailed_result.get("data", {}))
                                    
                                    # Collect data for auto-population
                                    target_muscles = detailed_data.get("targetMuscles", [])
                                    secondary_muscles = detailed_data.get("secondaryMuscles", [])
                                    equipments = detailed_data.get("equipments", [])
                                    body_parts = detailed_data.get("bodyParts", [])
                                    keywords = detailed_data.get("keywords", [])
                                    
                                    # Add muscles to our tracking set only if they exist in API response
                                    for muscle in target_muscles + secondary_muscles:
                                        if muscle and muscle.strip():
                                            all_muscles_found.add(muscle.strip().upper())
                                    
                                    # Add equipments to our tracking set
                                    for equipment in equipments:
                                        if equipment and equipment.strip():
                                            all_equipments_found.add(equipment.strip().upper())
                                    
                                    # Add body parts to our tracking set
                                    for body_part in body_parts:
                                        if body_part and body_part.strip():
                                            all_body_parts_found.add(body_part.strip().upper())
                                    
                                    # Add keywords to our tracking set
                                    for keyword in keywords:
                                        if keyword and keyword.strip():
                                            all_keywords_found.add(keyword.strip().lower())
                                    
                                    enriched_exercise["exercise_details"] = {
                                        "exerciseId": detailed_data.get("exerciseId"),
                                        "name": detailed_data.get("name"),
                                        "imageUrl": detailed_data.get("imageUrl"),
                                        "videoUrl": detailed_data.get("videoUrl"),
                                        "bodyParts": detailed_data.get("bodyParts", []),
                                        "equipments": detailed_data.get("equipments", []),
                                        "exerciseType": detailed_data.get("exerciseType"),
                                        "targetMuscles": detailed_data.get("targetMuscles", []),
                                        "secondaryMuscles": detailed_data.get("secondaryMuscles", []),
                                        "keywords": detailed_data.get("keywords", []),
                                        "overview": detailed_data.get("overview"),
                                        "instructions": detailed_data.get("instructions", []),
                                        "exerciseTips": detailed_data.get("exerciseTips", []),
                                        "variations": detailed_data.get("variations", [])
                                    }
                                    enriched_exercise["data_source"] = "exercisedb_api_detailed"
                                else:
                                    # Fallback to search data only
                                    first_match = exercise_data[0]
                                    enriched_exercise["exercise_details"] = {
                                        "exerciseId": first_match.get("exerciseId"),
                                        "name": first_match.get("name"),
                                        "imageUrl": first_match.get("imageUrl")
                                    }
                                    enriched_exercise["data_source"] = "exercisedb_api_search"
                            else:
                                enriched_exercise["exercise_details"] = None
                                enriched_exercise["data_source"] = "ai_only"
                        else:
                            enriched_exercise["exercise_details"] = None
                            enriched_exercise["data_source"] = "ai_only"
                    else:
                        enriched_exercise["exercise_details"] = None
                        enriched_exercise["data_source"] = "ai_only"
                        
                    enriched_exercises.append(enriched_exercise)
                
                enriched_day["exercises"] = enriched_exercises
                enriched_days.append(enriched_day)
            
            # Auto-populate lookup tables with newly found data
            muscles_created = self._auto_populate_muscles(all_muscles_found)
            equipments_created = self._auto_populate_equipments(all_equipments_found)
            body_parts_created = self._auto_populate_body_parts(all_body_parts_found)
            keywords_created = self._auto_populate_keywords(all_keywords_found)
            
            enriched_plan_data = plan_data.copy()
            enriched_plan_data["days"] = enriched_days
            
            logger.info("Successfully enriched workout plan with exercise data")
            enrichment_stats = self._get_enrichment_stats(enriched_days)
            enrichment_stats["muscles_auto_populated"] = muscles_created
            enrichment_stats["equipments_auto_populated"] = equipments_created
            enrichment_stats["body_parts_auto_populated"] = body_parts_created
            enrichment_stats["keywords_auto_populated"] = keywords_created
            
            return {
                "success": True,
                "data": enriched_plan_data,
                "message": "Workout plan enriched with exercise database information",
                "enrichment_stats": enrichment_stats
            }
            
        except Exception as e:
            logger.error(f"Error enriching workout plan: {e}")
            return {
                "success": False,
                "error": f"Enrichment error: {str(e)}",
                "message": "Failed to enrich workout plan with exercise data"
            }

    def _auto_populate_muscles(self, muscles_found: set) -> int:
        """
        Automatically populate the muscles table with any new muscles found during enrichment.
        
        Args:
            muscles_found (set): Set of muscle names found in exercise data
            
        Returns:
            int: Number of new muscles created
        """
        try:
            from api.models import Muscle
            
            if not muscles_found:
                return 0
            
            muscles_created = 0
            
            with transaction.atomic():
                for muscle_name in muscles_found:
                    if muscle_name and muscle_name.strip():
                        # Clean and format the muscle name
                        clean_name = muscle_name.strip().upper()
                        
                        # Use get_or_create to avoid duplicates
                        muscle, created = Muscle.objects.get_or_create(
                            name=clean_name,
                            defaults={'name': clean_name}
                        )
                        
                        if created:
                            muscles_created += 1
                            logger.info(f"Auto-created muscle: {clean_name}")
            
            if muscles_created > 0:
                logger.info(f"Auto-populated {muscles_created} new muscles during workout plan enrichment")
            
            return muscles_created
            
        except Exception as e:
            logger.error(f"Error auto-populating muscles: {e}")
            # Don't fail the entire enrichment process if muscle population fails
            return 0

    def _auto_populate_equipments(self, equipments_found: set) -> int:
        """
        Automatically populate the equipments table with any new equipment found during enrichment.
        
        Args:
            equipments_found (set): Set of equipment names found in exercise data
            
        Returns:
            int: Number of new equipments created
        """
        try:
            from api.models import Equipment
            
            if not equipments_found:
                return 0
            
            equipments_created = 0
            
            with transaction.atomic():
                for equipment_name in equipments_found:
                    if equipment_name and equipment_name.strip():
                        # Clean and format the equipment name
                        clean_name = equipment_name.strip().upper()
                        
                        # Use get_or_create to avoid duplicates
                        equipment, created = Equipment.objects.get_or_create(
                            name=clean_name,
                            defaults={'name': clean_name}
                        )
                        
                        if created:
                            equipments_created += 1
                            logger.info(f"Auto-created equipment: {clean_name}")
            
            if equipments_created > 0:
                logger.info(f"Auto-populated {equipments_created} new equipments during workout plan enrichment")
            
            return equipments_created
            
        except Exception as e:
            logger.error(f"Error auto-populating equipments: {e}")
            # Don't fail the entire enrichment process if equipment population fails
            return 0

    def _auto_populate_body_parts(self, body_parts_found: set) -> int:
        """
        Automatically populate the body_parts table with any new body parts found during enrichment.
        
        Args:
            body_parts_found (set): Set of body part names found in exercise data
            
        Returns:
            int: Number of new body parts created
        """
        try:
            from api.models import BodyPart
            
            if not body_parts_found:
                return 0
            
            body_parts_created = 0
            
            with transaction.atomic():
                for body_part_name in body_parts_found:
                    if body_part_name and body_part_name.strip():
                        # Clean and format the body part name
                        clean_name = body_part_name.strip().upper()
                        
                        # Use get_or_create to avoid duplicates
                        body_part, created = BodyPart.objects.get_or_create(
                            name=clean_name,
                            defaults={'name': clean_name}
                        )
                        
                        if created:
                            body_parts_created += 1
                            logger.info(f"Auto-created body part: {clean_name}")
            
            if body_parts_created > 0:
                logger.info(f"Auto-populated {body_parts_created} new body parts during workout plan enrichment")
            
            return body_parts_created
            
        except Exception as e:
            logger.error(f"Error auto-populating body parts: {e}")
            # Don't fail the entire enrichment process if body part population fails
            return 0

    def _auto_populate_keywords(self, keywords_found: set) -> int:
        """
        Automatically populate the keywords table with any new keywords found during enrichment.
        
        Args:
            keywords_found (set): Set of keywords found in exercise data
            
        Returns:
            int: Number of new keywords created
        """
        try:
            from api.models import Keyword
            
            if not keywords_found:
                return 0
            
            keywords_created = 0
            
            with transaction.atomic():
                for keyword_text in keywords_found:
                    if keyword_text and keyword_text.strip():
                        # Clean and format the keyword (keep original case for keywords)
                        clean_keyword = keyword_text.strip().lower()
                        
                        # Use get_or_create to avoid duplicates
                        keyword, created = Keyword.objects.get_or_create(
                            keyword=clean_keyword,
                            defaults={'keyword': clean_keyword}
                        )
                        
                        if created:
                            keywords_created += 1
                            logger.info(f"Auto-created keyword: {clean_keyword}")
            
            if keywords_created > 0:
                logger.info(f"Auto-populated {keywords_created} new keywords during workout plan enrichment")
            
            return keywords_created
            
        except Exception as e:
            logger.error(f"Error auto-populating keywords: {e}")
            # Don't fail the entire enrichment process if keyword population fails
            return 0

    def _get_enrichment_stats(self, enriched_days: List[Dict]) -> Dict:
        """
        Calculate statistics about the enrichment process.
        
        Args:
            enriched_days (list): List of enriched day objects
            
        Returns:
            dict: Statistics about the enrichment
        """
        total_exercises = 0
        detailed_enriched = 0
        search_enriched = 0
        ai_only = 0
        
        for day in enriched_days:
            exercises = day.get("exercises", [])
            total_exercises += len(exercises)
            
            for exercise in exercises:
                data_source = exercise.get("data_source", "ai_only")
                if data_source == "exercisedb_api_detailed":
                    detailed_enriched += 1
                elif data_source == "exercisedb_api_search":
                    search_enriched += 1
                else:
                    ai_only += 1
        
        total_enriched = detailed_enriched + search_enriched
        enrichment_rate = (total_enriched / total_exercises * 100) if total_exercises > 0 else 0
        
        return {
            "total_exercises": total_exercises,
            "detailed_enriched": detailed_enriched,
            "search_enriched": search_enriched,
            "ai_only": ai_only,
            "total_enriched": total_enriched,
            "enrichment_rate": round(enrichment_rate, 2),
            "muscles_auto_populated": 0,  # Will be updated by enrich_workout_plan
            "equipments_auto_populated": 0,  # Will be updated by enrich_workout_plan
            "body_parts_auto_populated": 0,  # Will be updated by enrich_workout_plan
            "keywords_auto_populated": 0  # Will be updated by enrich_workout_plan
        }

    def get_exercise_suggestions(self, exercise_names: List[str]) -> Dict:
        """
        Get exercise data for a list of exercise names from AI-generated plans.
        
        Args:
            exercise_names (list): List of exercise names to look up
            
        Returns:
            dict: Results for each exercise name
        """
        try:
            results = {}
            
            for exercise_name in exercise_names:
                search_result = self.search_exercises(exercise_name)
                results[exercise_name] = search_result
                
            logger.info(f"Retrieved suggestions for {len(exercise_names)} exercises")
            return {
                "success": True,
                "data": results,
                "message": f"Retrieved exercise data for {len(exercise_names)} exercises"
            }
            
        except Exception as e:
            logger.error(f"Error getting exercise suggestions: {e}")
            return {
                "success": False,
                "error": f"Suggestion error: {str(e)}",
                "message": "Failed to get exercise suggestions"
            }

    def get_equipments(self) -> Dict:
        """
        Get all available equipment types from ExerciseDB API.
        
        API Endpoint: GET /api/v1/equipments
        Response Structure:
        {
            "success": true,
            "data": [
                {
                    "name": str,
                    "imageUrl": str
                }
            ]
        }
        
        Returns:
            dict: API response containing equipment data (28 equipment types)
        """
        try:
            url = f"{self.base_url}/equipments"
            
            response = requests.get(url, headers=self.headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Successfully retrieved {len(data.get('data', []))} equipment types")
                return {
                    "success": True,
                    "data": data,
                    "message": "Equipment types retrieved successfully"
                }
            else:
                logger.warning(f"Failed to get equipment types. Status: {response.status_code}")
                return {
                    "success": False,
                    "error": f"API returned status code: {response.status_code}",
                    "message": "Failed to retrieve equipment types"
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error getting equipment types: {e}")
            return {
                "success": False,
                "error": f"Request error: {str(e)}",
                "message": "Failed to connect to ExerciseDB API"
            }
        except Exception as e:
            logger.error(f"Unexpected error getting equipment types: {e}")
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "message": "An unexpected error occurred"
            }

    def get_exercise_types(self) -> Dict:
        """
        Get all available exercise types from ExerciseDB API.
        
        API Endpoint: GET /api/v1/exercisetypes
        Response Structure:
        {
            "success": true,
            "data": [
                {
                    "name": str,
                    "imageUrl": str
                }
            ]
        }
        
        Returns:
            dict: API response containing exercise type data (7 types: STRENGTH, CARDIO, PLYOMETRICS, STRETCHING, WEIGHTLIFTING, YOGA, AEROBIC)
        """
        try:
            url = f"{self.base_url}/exercisetypes"
            
            response = requests.get(url, headers=self.headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Successfully retrieved {len(data.get('data', []))} exercise types")
                return {
                    "success": True,
                    "data": data,
                    "message": "Exercise types retrieved successfully"
                }
            else:
                logger.warning(f"Failed to get exercise types. Status: {response.status_code}")
                return {
                    "success": False,
                    "error": f"API returned status code: {response.status_code}",
                    "message": "Failed to retrieve exercise types"
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error getting exercise types: {e}")
            return {
                "success": False,
                "error": f"Request error: {str(e)}",
                "message": "Failed to connect to ExerciseDB API"
            }
        except Exception as e:
            logger.error(f"Unexpected error getting exercise types: {e}")
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "message": "An unexpected error occurred"
            }

    def get_bodyparts(self) -> Dict:
        """
        Get all available body parts from ExerciseDB API.
        
        API Endpoint: GET /api/v1/bodyparts
        Response Structure:
        {
            "success": true,
            "data": [
                {
                    "name": str,
                    "imageUrl": str
                }
            ]
        }
        
        Returns:
            dict: API response containing body part data (18 body parts: BACK, CHEST, SHOULDERS, etc.)
        """
        try:
            url = f"{self.base_url}/bodyparts"
            
            response = requests.get(url, headers=self.headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Successfully retrieved {len(data.get('data', []))} body parts")
                return {
                    "success": True,
                    "data": data,
                    "message": "Body parts retrieved successfully"
                }
            else:
                logger.warning(f"Failed to get body parts. Status: {response.status_code}")
                return {
                    "success": False,
                    "error": f"API returned status code: {response.status_code}",
                    "message": "Failed to retrieve body parts"
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error getting body parts: {e}")
            return {
                "success": False,
                "error": f"Request error: {str(e)}",
                "message": "Failed to connect to ExerciseDB API"
            }
        except Exception as e:
            logger.error(f"Unexpected error getting body parts: {e}")
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "message": "An unexpected error occurred"
            }

    def get_muscles(self) -> Dict:
        """
        Get all available muscle groups from ExerciseDB API.
        
        API Endpoint: GET /api/v1/muscles
        Response Structure:
        {
            "success": true,
            "data": [
                {
                    "name": str
                }
            ]
        }
        
        Returns:
            dict: API response containing muscle data (3 muscle groups)
        """
        try:
            url = f"{self.base_url}/muscles"
            
            response = requests.get(url, headers=self.headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Successfully retrieved {len(data.get('data', []))} muscle groups")
                return {
                    "success": True,
                    "data": data,
                    "message": "Muscle groups retrieved successfully"
                }
            else:
                logger.warning(f"Failed to get muscle groups. Status: {response.status_code}")
                return {
                    "success": False,
                    "error": f"API returned status code: {response.status_code}",
                    "message": "Failed to retrieve muscle groups"
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error getting muscle groups: {e}")
            return {
                "success": False,
                "error": f"Request error: {str(e)}",
                "message": "Failed to connect to ExerciseDB API"
            }
        except Exception as e:
            logger.error(f"Unexpected error getting muscle groups: {e}")
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "message": "An unexpected error occurred"
            }

    def get_reference_data(self) -> Dict:
        """
        Get all reference data (equipments, exercise types, body parts, muscles) in one call.
        This is useful for populating filter options in the frontend.
        
        Returns:
            dict: Combined reference data from all endpoints
        """
        try:
            logger.info("Fetching all reference data...")
            
            # Get all reference data concurrently would be ideal, but for simplicity we'll do them sequentially
            equipments_result = self.get_equipments()
            exercise_types_result = self.get_exercise_types()
            bodyparts_result = self.get_bodyparts()
            muscles_result = self.get_muscles()
            
            # Check if all requests were successful
            all_successful = all([
                equipments_result.get('success', False),
                exercise_types_result.get('success', False),
                bodyparts_result.get('success', False),
                muscles_result.get('success', False)
            ])
            
            if all_successful:
                logger.info("Successfully retrieved all reference data")
                return {
                    "success": True,
                    "data": {
                        "equipments": equipments_result['data'].get('data', []),
                        "exercise_types": exercise_types_result['data'].get('data', []),
                        "bodyparts": bodyparts_result['data'].get('data', []),
                        "muscles": muscles_result['data'].get('data', [])
                    },
                    "message": "All reference data retrieved successfully",
                    "counts": {
                        "equipments": len(equipments_result['data'].get('data', [])),
                        "exercise_types": len(exercise_types_result['data'].get('data', [])),
                        "bodyparts": len(bodyparts_result['data'].get('data', [])),
                        "muscles": len(muscles_result['data'].get('data', []))
                    }
                }
            else:
                # Collect errors from failed requests
                errors = []
                if not equipments_result.get('success'):
                    errors.append(f"Equipments: {equipments_result.get('error', 'Unknown error')}")
                if not exercise_types_result.get('success'):
                    errors.append(f"Exercise Types: {exercise_types_result.get('error', 'Unknown error')}")
                if not bodyparts_result.get('success'):
                    errors.append(f"Body Parts: {bodyparts_result.get('error', 'Unknown error')}")
                if not muscles_result.get('success'):
                    errors.append(f"Muscles: {muscles_result.get('error', 'Unknown error')}")
                
                logger.warning(f"Some reference data requests failed: {'; '.join(errors)}")
                return {
                    "success": False,
                    "error": "Some reference data requests failed",
                    "details": errors,
                    "message": "Failed to retrieve complete reference data"
                }
                
        except Exception as e:
            logger.error(f"Unexpected error getting reference data: {e}")
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "message": "An unexpected error occurred while fetching reference data"
            }

    def get_exercises_by_filters(self, equipment: Optional[str] = None, 
                                bodypart: Optional[str] = None, 
                                exercise_type: Optional[str] = None,
                                limit: int = 20) -> Dict:
        """
        Get exercises filtered by equipment, body part, or exercise type.
        This combines the basic exercise search with reference data filtering.
        
        Args:
            equipment (str, optional): Equipment type to filter by
            bodypart (str, optional): Body part to filter by  
            exercise_type (str, optional): Exercise type to filter by
            limit (int): Maximum number of exercises to return
            
        Returns:
            dict: Filtered exercise results
        """
        try:
            # Build search terms based on filters
            search_terms = []
            
            if equipment:
                search_terms.append(equipment.lower())
            if bodypart:
                search_terms.append(bodypart.lower())
            if exercise_type:
                search_terms.append(exercise_type.lower())
            
            if search_terms:
                # Use search endpoint with combined terms
                search_term = " ".join(search_terms)
                result = self.search_exercises(search_term)
                
                if result.get('success', False):
                    # Limit the results
                    exercises = result['data'].get('data', [])
                    limited_exercises = exercises[:limit]
                    
                    result['data']['data'] = limited_exercises
                    result['applied_filters'] = {
                        "equipment": equipment,
                        "bodypart": bodypart,
                        "exercise_type": exercise_type,
                        "limit": limit
                    }
                    result['message'] = f"Found {len(limited_exercises)} exercises matching filters"
                    
                return result
            else:
                # No filters provided, get general exercises
                return self.get_exercises(limit=limit)
                
        except Exception as e:
            logger.error(f"Error filtering exercises: {e}")
            return {
                "success": False,
                "error": f"Filter error: {str(e)}",
                "message": "Failed to filter exercises"
            }