import requests
from decouple import config
import logging
import json
from typing import Dict, List, Optional, Union

logger = logging.getLogger(__name__)


class ExerciseDBService:
    """
    Service class for integrating with ExerciseDB API.
    Handles exercise data retrieval, search, and integration with AI-generated workout plans.
    """
    
    def __init__(self):
        """Initialize the ExerciseDB API client with API key and base configuration."""
        try:
            self.api_key = config('EXERCISEDB_API_KEY', default="e54b6f7f15mshdf7311120e07d4fp1e4a2djsn7ec38821b9ee")
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
        Test the API connection using the liveness endpoint.
        
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
            
            for day in days:
                enriched_day = day.copy()
                exercises = day.get("exercises", [])
                enriched_exercises = []
                
                for exercise in exercises:
                    exercise_name = exercise.get("exercise_name", "")
                    
                    # Search for exercise data
                    search_result = self.search_exercises(exercise_name)
                    
                    enriched_exercise = exercise.copy()
                    
                    if search_result.get("success", False):
                        exercise_data = search_result.get("data", {}).get("data", [])
                        if exercise_data:
                            # Take the first matching exercise
                            first_match = exercise_data[0]
                            enriched_exercise["exercise_details"] = {
                                "id": first_match.get("id"),
                                "name": first_match.get("name"),
                                "target": first_match.get("target"),
                                "bodyPart": first_match.get("bodyPart"),
                                "equipment": first_match.get("equipment"),
                                "gifUrl": first_match.get("gifUrl"),
                                "instructions": first_match.get("instructions", []),
                                "secondaryMuscles": first_match.get("secondaryMuscles", [])
                            }
                            enriched_exercise["data_source"] = "exercisedb_api"
                        else:
                            enriched_exercise["exercise_details"] = None
                            enriched_exercise["data_source"] = "ai_only"
                    else:
                        enriched_exercise["exercise_details"] = None
                        enriched_exercise["data_source"] = "ai_only"
                        
                    enriched_exercises.append(enriched_exercise)
                
                enriched_day["exercises"] = enriched_exercises
                enriched_days.append(enriched_day)
            
            enriched_plan_data = plan_data.copy()
            enriched_plan_data["days"] = enriched_days
            
            logger.info("Successfully enriched workout plan with exercise data")
            return {
                "success": True,
                "data": enriched_plan_data,
                "message": "Workout plan enriched with exercise database information",
                "enrichment_stats": self._get_enrichment_stats(enriched_days)
            }
            
        except Exception as e:
            logger.error(f"Error enriching workout plan: {e}")
            return {
                "success": False,
                "error": f"Enrichment error: {str(e)}",
                "message": "Failed to enrich workout plan with exercise data"
            }

    def _get_enrichment_stats(self, enriched_days: List[Dict]) -> Dict:
        """
        Calculate statistics about the enrichment process.
        
        Args:
            enriched_days (list): List of enriched day objects
            
        Returns:
            dict: Statistics about the enrichment
        """
        total_exercises = 0
        enriched_exercises = 0
        
        for day in enriched_days:
            exercises = day.get("exercises", [])
            total_exercises += len(exercises)
            
            for exercise in exercises:
                if exercise.get("data_source") == "exercisedb_api":
                    enriched_exercises += 1
        
        enrichment_rate = (enriched_exercises / total_exercises * 100) if total_exercises > 0 else 0
        
        return {
            "total_exercises": total_exercises,
            "enriched_exercises": enriched_exercises,
            "enrichment_rate": round(enrichment_rate, 2),
            "missing_data": total_exercises - enriched_exercises
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
        
        Returns:
            dict: API response containing equipment data
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
        
        Returns:
            dict: API response containing exercise type data
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
        
        Returns:
            dict: API response containing body part data
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
        
        Returns:
            dict: API response containing muscle data
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