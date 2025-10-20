/**
 * AI Workout Plan API Service
 * Handles all API calls related to AI-generated workout plans
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api';

// TypeScript interfaces
export interface ExerciseDetails {
  exerciseId: string;
  name: string;
  imageUrl: string;
  videoUrl: string;
  bodyParts: string[];
  equipments: string[];
  exerciseType: string;
  targetMuscles: string[];
  secondaryMuscles: string[];
  keywords: string[];
  overview: string;
  instructions: string[];
  exerciseTips: string[];
  variations: string[];
  relatedExerciseIds: string[];
}

export interface Exercise {
  exercise_name: string;
  sets: number;
  reps: string;
  exercise_details?: ExerciseDetails;
  data_source?: string;
  match_confidence?: string;
  matched_exercise_name?: string;
  search_strategy?: string;
}

export interface WorkoutDay {
  day_number: number;
  day_name: string;
  exercises: Exercise[];
}

export interface WorkoutPlanData {
  plan_name: string;
  plan_description: string;
  days: WorkoutDay[];
}

export interface EnrichmentStats {
  total_exercises: number;
  detailed_enriched: number;
  search_enriched: number;
  ai_only: number;
  total_enriched: number;
  enrichment_rate: number;
  high_confidence_matches: number;
  medium_confidence_matches: number;
  no_matches: number;
  high_confidence_rate: number;
  muscles_auto_populated: number;
  equipments_auto_populated: number;
  body_parts_auto_populated: number;
  keywords_auto_populated: number;
}

export interface WorkoutPlan {
  id: string;
  user: string;
  name: string;
  description: string;
  workout_plan_data: {
    success: boolean;
    data: WorkoutPlanData;
    message: string;
    enrichment_stats: EnrichmentStats;
  };
  created_at: string;
}

export interface GenerateWorkoutPlanRequest {
  user_id: string;
  user_goal: string;
  experience_level: 'beginner' | 'intermediate' | 'advanced';
  days_per_week: number;
  save_plan?: boolean;
}

export interface GenerateWorkoutPlanResponse {
  success: boolean;
  data: WorkoutPlanData;
  enrichment_stats: EnrichmentStats;
  message: string;
  user_id: string;
  generation_params: {
    user_goal: string;
    experience_level: string;
    days_per_week: number;
  };
  saved_plan_id?: string;
}

/**
 * Generate a new AI workout plan
 */
export async function generateWorkoutPlan(
  userId: string,
  userGoal: string,
  experienceLevel: 'beginner' | 'intermediate' | 'advanced',
  daysPerWeek: number,
  savePlan: boolean = true
): Promise<GenerateWorkoutPlanResponse> {
  try {
    const requestData: GenerateWorkoutPlanRequest = {
      user_id: userId,
      user_goal: userGoal,
      experience_level: experienceLevel,
      days_per_week: daysPerWeek,
      save_plan: savePlan,
    };

    console.log('Generating workout plan with:', requestData);

    const response = await fetch(`${API_BASE_URL}/generate-workout-plan/`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestData),
    });

    console.log('Generate workout plan response status:', response.status);

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(`Failed to generate workout plan: ${JSON.stringify(errorData)}`);
    }

    const data = await response.json();
    console.log('Workout plan generated:', data);
    return data;
  } catch (error) {
    console.error('Error generating workout plan:', error);
    throw error;
  }
}

/**
 * Get all saved workout plans for the authenticated user
 */
export async function getSavedWorkoutPlans(): Promise<WorkoutPlan[]> {
  try {
    const response = await fetch(`${API_BASE_URL}/workout-plans/`, {
      method: 'GET',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    console.log('Get saved workout plans response status:', response.status);

    if (!response.ok) {
      throw new Error(`Failed to fetch saved workout plans: ${response.status}`);
    }

    const data = await response.json();
    console.log('Saved workout plans fetched:', data);

    // Handle both paginated and direct array responses
    return data.results || data;
  } catch (error) {
    console.error('Error fetching saved workout plans:', error);
    throw error;
  }
}

/**
 * Get a specific workout plan by ID
 */
export async function getWorkoutPlanDetail(planId: string): Promise<WorkoutPlan> {
  try {
    const response = await fetch(`${API_BASE_URL}/workout-plans/${planId}/`, {
      method: 'GET',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    console.log('Get workout plan detail response status:', response.status);

    if (!response.ok) {
      throw new Error(`Failed to fetch workout plan: ${response.status}`);
    }

    const data = await response.json();
    console.log('Workout plan detail fetched:', data);
    return data;
  } catch (error) {
    console.error('Error fetching workout plan detail:', error);
    throw error;
  }
}
