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

    def _enhanced_exercise_search(self, exercise_name: str) -> Dict:
        """
        Enhanced exercise search with multiple strategies for better matching.
        
        Tries different search approaches:
        1. Direct search with full name
        2. Search with cleaned name (remove hyphens, underscores)
        3. Search with individual words
        4. Search with partial terms
        
        Args:
            exercise_name (str): Exercise name to search for
            
        Returns:
            dict: Best search result found, or failure result
        """
        try:
            if not exercise_name or not exercise_name.strip():
                return {
                    "success": False,
                    "error": "Empty exercise name",
                    "message": "Exercise name cannot be empty"
                }
            
            search_strategies = []
            
            # Strategy 1: Direct search with original name
            search_strategies.append(("direct", exercise_name.strip()))
            
            # Strategy 2: Cleaned name (normalize spaces, remove special chars)
            cleaned_name = exercise_name.strip().replace('-', ' ').replace('_', ' ')
            cleaned_name = ' '.join(cleaned_name.split())  # Normalize spaces
            if cleaned_name != exercise_name.strip():
                search_strategies.append(("cleaned", cleaned_name))
            
            # Strategy 3: Search with individual significant words (longer than 2 chars)
            words = [word for word in cleaned_name.split() if len(word) > 2]
            if len(words) > 1:
                for word in words:
                    search_strategies.append(("word", word))
            
            # Strategy 4: Partial search with first significant word + last word
            if len(words) > 1:
                partial_search = f"{words[0]} {words[-1]}"
                if partial_search != cleaned_name:
                    search_strategies.append(("partial", partial_search))
            
            best_result = None
            best_match_count = 0
            
            for strategy_name, search_term in search_strategies:
                logger.debug(f"Trying {strategy_name} search for '{exercise_name}' with term: '{search_term}'")
                
                search_result = self.search_exercises(search_term)
                
                if search_result.get("success", False):
                    exercise_data = search_result.get("data", {}).get("data", [])
                    match_count = len(exercise_data)
                    
                    if match_count > 0:
                        # Find best match using intelligent matching
                        best_match = self._find_best_exercise_match(exercise_name, exercise_data)
                        
                        if best_match:
                            logger.info(f"Strategy '{strategy_name}' found {match_count} results for '{exercise_name}'")
                            return {
                                "success": True,
                                "data": {"data": exercise_data},
                                "best_match": best_match,
                                "strategy_used": strategy_name,
                                "search_term": search_term,
                                "message": f"Found match using {strategy_name} search"
                            }
                        elif match_count > best_match_count:
                            # Keep track of best result even if no good match found
                            best_result = search_result
                            best_match_count = match_count
                    else:
                        logger.debug(f"Strategy '{strategy_name}' returned no results")
                else:
                    logger.debug(f"Strategy '{strategy_name}' failed: {search_result.get('message', 'Unknown error')}")
            
            # If no good matches found, return the best result we got
            if best_result:
                logger.warning(f"No intelligent matches found for '{exercise_name}', returning best result with {best_match_count} exercises")
                return {
                    "success": True,
                    "data": best_result["data"],
                    "best_match": None,
                    "strategy_used": "fallback",
                    "message": f"Found {best_match_count} results but no good matches"
                }
            
            logger.warning(f"All search strategies failed for exercise: '{exercise_name}'")
            return {
                "success": False,
                "error": "No search results found",
                "message": f"No exercises found matching '{exercise_name}'"
            }
            
        except Exception as e:
            logger.error(f"Error in enhanced exercise search for '{exercise_name}': {e}")
            return {
                "success": False,
                "error": f"Search error: {str(e)}",
                "message": "An error occurred during exercise search"
            }

    def _find_best_exercise_match(self, target_exercise_name: str, search_results: List[Dict]) -> Optional[Dict]:
        """
        Find the best matching exercise from search results using intelligent matching.
        
        Uses multiple scoring criteria:
        1. Exact name match (highest priority)
        2. Name similarity (fuzzy matching)
        3. Keyword matching
        4. Partial name matching
        
        Args:
            target_exercise_name (str): The exercise name from AI-generated workout
            search_results (list): List of exercises from search API
            
        Returns:
            dict or None: Best matching exercise or None if no good match found
        """
        try:
            if not search_results or not target_exercise_name:
                return None
            
            target_name_lower = target_exercise_name.lower().strip()
            target_words = set(target_name_lower.split())
            
            best_match = None
            best_score = 0
            
            for exercise in search_results:
                exercise_name = exercise.get('name', '').lower().strip()
                exercise_words = set(exercise_name.split())
                
                score = 0
                
                # 1. Exact match (highest priority)
                if target_name_lower == exercise_name:
                    score += 100
                
                # 2. Exact substring match
                elif target_name_lower in exercise_name or exercise_name in target_name_lower:
                    score += 80
                
                # 3. Word overlap scoring
                common_words = target_words.intersection(exercise_words)
                if common_words:
                    word_overlap_ratio = len(common_words) / max(len(target_words), len(exercise_words))
                    score += word_overlap_ratio * 60
                
                # 4. Partial word matching (for abbreviations, etc.)
                for target_word in target_words:
                    for exercise_word in exercise_words:
                        if len(target_word) >= 3 and len(exercise_word) >= 3:
                            if target_word in exercise_word or exercise_word in target_word:
                                score += 20
                
                # 5. Character similarity (simple Levenshtein-like scoring)
                if len(target_name_lower) > 0 and len(exercise_name) > 0:
                    char_similarity = self._calculate_string_similarity(target_name_lower, exercise_name)
                    score += char_similarity * 30
                
                # 6. Bonus for exercise type matching common patterns
                # This helps with exercises like "push-up" vs "push up" or "pushup"
                normalized_target = target_name_lower.replace('-', ' ').replace('_', ' ')
                normalized_exercise = exercise_name.replace('-', ' ').replace('_', ' ')
                if normalized_target == normalized_exercise:
                    score += 50
                
                logger.debug(f"Exercise '{exercise_name}' scored {score:.2f} for target '{target_exercise_name}'")
                
                # Update best match if this exercise scores higher
                if score > best_score and score >= 30:  # Minimum threshold for acceptable match
                    best_score = score
                    best_match = exercise
            
            if best_match:
                logger.info(f"Best match for '{target_exercise_name}': '{best_match.get('name')}' (score: {best_score:.2f})")
            else:
                logger.warning(f"No suitable match found for '{target_exercise_name}' (best score: {best_score:.2f})")
            
            return best_match
            
        except Exception as e:
            logger.error(f"Error finding best exercise match: {e}")
            return None

    def _calculate_string_similarity(self, str1: str, str2: str) -> float:
        """
        Calculate similarity between two strings using a simple character-based approach.
        
        Args:
            str1 (str): First string
            str2 (str): Second string
            
        Returns:
            float: Similarity score between 0.0 and 1.0
        """
        try:
            if not str1 or not str2:
                return 0.0
            
            if str1 == str2:
                return 1.0
            
            # Simple character overlap approach
            set1 = set(str1.lower())
            set2 = set(str2.lower())
            
            intersection = len(set1.intersection(set2))
            union = len(set1.union(set2))
            
            return intersection / union if union > 0 else 0.0
            
        except Exception:
            return 0.0

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
                    
                    # Enhanced search for exercise data with multiple strategies and intelligent matching
                    search_result = self._enhanced_exercise_search(exercise_name)
                    
                    enriched_exercise = exercise.copy()
                    
                    if search_result.get("success", False):
                        best_match = search_result.get("best_match")
                        strategy_used = search_result.get("strategy_used", "unknown")
                        
                        if best_match:
                            exercise_id = best_match.get("exerciseId")
                            if exercise_id:
                                logger.info(f"Found match for '{exercise_name}' using {strategy_used} strategy: '{best_match.get('name')}' (ID: {exercise_id})")
                                
                                # Get detailed exercise information using the matched exercise ID
                                detailed_result = self.get_exercise_by_id(exercise_id)
                                if detailed_result.get("success", False):
                                    detailed_data = detailed_result.get("data", {}).get("data", detailed_result.get("data", {}))

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
                                        "variations": detailed_data.get("variations", []),
                                        "relatedExerciseIds": detailed_data.get("relatedExerciseIds", [])
                                    }
                                    enriched_exercise["data_source"] = "exercisedb_api_detailed"
                                    enriched_exercise["match_confidence"] = "high"
                                    enriched_exercise["matched_exercise_name"] = detailed_data.get("name")
                                    enriched_exercise["search_strategy"] = strategy_used
                                    logger.info(f"Successfully enriched '{exercise_name}' with detailed data")
                                else:
                                    # Fallback to search data only if detailed fetch fails
                                    enriched_exercise["exercise_details"] = {
                                        "exerciseId": best_match.get("exerciseId"),
                                        "name": best_match.get("name"),
                                        "imageUrl": best_match.get("imageUrl")
                                    }
                                    enriched_exercise["data_source"] = "exercisedb_api_search"
                                    enriched_exercise["match_confidence"] = "medium"
                                    enriched_exercise["matched_exercise_name"] = best_match.get("name")
                                    enriched_exercise["search_strategy"] = strategy_used
                                    logger.warning(f"Detailed fetch failed for '{exercise_name}', using search data only")
                            else:
                                enriched_exercise["exercise_details"] = None
                                enriched_exercise["data_source"] = "ai_only"
                                enriched_exercise["match_confidence"] = "none"
                                enriched_exercise["search_strategy"] = strategy_used
                                logger.warning(f"No exercise ID found for best match: '{exercise_name}'")
                        else:
                            # Search succeeded but no good match found
                            enriched_exercise["exercise_details"] = None
                            enriched_exercise["data_source"] = "ai_only"
                            enriched_exercise["match_confidence"] = "none"
                            enriched_exercise["search_strategy"] = strategy_used
                            logger.warning(f"Search found results but no suitable match for exercise: '{exercise_name}'")
                    else:
                        enriched_exercise["exercise_details"] = None
                        enriched_exercise["data_source"] = "ai_only" 
                        enriched_exercise["match_confidence"] = "none"
                        enriched_exercise["search_strategy"] = "failed"
                        logger.warning(f"Enhanced search failed for exercise: '{exercise_name}' - {search_result.get('message', 'Unknown error')}")
                        
                    enriched_exercises.append(enriched_exercise)
                
                enriched_day["exercises"] = enriched_exercises
                enriched_days.append(enriched_day)

            enriched_plan_data = plan_data.copy()
            enriched_plan_data["days"] = enriched_days

            logger.info("Successfully enriched workout plan with exercise data")
            enrichment_stats = self._get_enrichment_stats(enriched_days)
            
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
        
        # Match confidence tracking
        high_confidence_matches = 0
        medium_confidence_matches = 0
        no_matches = 0
        
        for day in enriched_days:
            exercises = day.get("exercises", [])
            total_exercises += len(exercises)
            
            for exercise in exercises:
                data_source = exercise.get("data_source", "ai_only")
                match_confidence = exercise.get("match_confidence", "none")
                
                # Count by data source
                if data_source == "exercisedb_api_detailed":
                    detailed_enriched += 1
                elif data_source == "exercisedb_api_search":
                    search_enriched += 1
                else:
                    ai_only += 1
                
                # Count by match confidence
                if match_confidence == "high":
                    high_confidence_matches += 1
                elif match_confidence == "medium":
                    medium_confidence_matches += 1
                else:
                    no_matches += 1
        
        total_enriched = detailed_enriched + search_enriched
        enrichment_rate = (total_enriched / total_exercises * 100) if total_exercises > 0 else 0
        high_confidence_rate = (high_confidence_matches / total_exercises * 100) if total_exercises > 0 else 0
        
        return {
            "total_exercises": total_exercises,
            "detailed_enriched": detailed_enriched,
            "search_enriched": search_enriched,
            "ai_only": ai_only,
            "total_enriched": total_enriched,
            "enrichment_rate": round(enrichment_rate, 2),
            "high_confidence_matches": high_confidence_matches,
            "medium_confidence_matches": medium_confidence_matches,
            "no_matches": no_matches,
            "high_confidence_rate": round(high_confidence_rate, 2)
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