/**
 * Workout Logs API Service
 * Handles all API calls related to user workout logs
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api';

// TypeScript interfaces
export interface WorkoutLog {
  id: string;
  date_performed: string; // ISO timestamp
  sets_performed: number;
  reps_performed: number;
  duration_minutes?: number;
  calories_burned?: number;
  perceived_effort?: number;
  user_id: string;
  exercise_name?: string;
  weight?: number;
  exercise_data?: any; // JSON data for custom info
}

export interface CreateWorkoutData {
  date_performed: string;
  sets_performed: number;
  reps_performed: number;
  duration_minutes?: number;
  calories_burned?: number;
  perceived_effort?: number;
  exercise_name?: string;
  weight?: number;
  exercise_data?: any;
}

export interface UpdateWorkoutData extends Partial<CreateWorkoutData> {}

/**
 * Get all workouts for the authenticated user
 */
export async function getWorkouts(): Promise<WorkoutLog[]> {
  try {
    const response = await fetch(`${API_BASE_URL}/workouts/`, {
      method: 'GET',
      credentials: 'include', // include session cookies
      headers: { 'Content-Type': 'application/json' },
    });

    if (!response.ok) throw new Error(`Failed to fetch workouts: ${response.status}`);

    const data = await response.json();
    console.log('Workouts fetched:', data);
    return data.results || data;
  } catch (error) {
    console.error('Error fetching workouts:', error);
    throw error;
  }
}

/**
 * Get a specific workout by ID
 */
export async function getWorkout(workoutId: string): Promise<WorkoutLog> {
  try {
    const response = await fetch(`${API_BASE_URL}/workouts/${workoutId}/`, {
      method: 'GET',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
    });

    if (!response.ok) throw new Error(`Failed to fetch workout: ${response.status}`);

    const data = await response.json();
    console.log('Workout fetched:', data);
    return data;
  } catch (error) {
    console.error('Error fetching workout:', error);
    throw error;
  }
}

/**
 * Create a new workout
 */
export async function createWorkout(workoutData: CreateWorkoutData): Promise<WorkoutLog> {
  try {
    const response = await fetch(`${API_BASE_URL}/workouts/`, {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(workoutData),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(`Failed to create workout: ${JSON.stringify(errorData)}`);
    }

    const data = await response.json();
    console.log('Workout created:', data);
    return data;
  } catch (error) {
    console.error('Error creating workout:', error);
    throw error;
  }
}

/**
 * Update an existing workout
 */
export async function updateWorkout(workoutId: string, workoutData: UpdateWorkoutData): Promise<WorkoutLog> {
  try {
    const response = await fetch(`${API_BASE_URL}/workouts/${workoutId}/`, {
      method: 'PATCH',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(workoutData),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(`Failed to update workout: ${JSON.stringify(errorData)}`);
    }

    const data = await response.json();
    console.log('Workout updated:', data);
    return data;
  } catch (error) {
    console.error('Error updating workout:', error);
    throw error;
  }
}

/**
 * Delete a workout
 */
export async function deleteWorkout(workoutId: string): Promise<void> {
  try {
    const response = await fetch(`${API_BASE_URL}/workouts/${workoutId}/`, {
      method: 'DELETE',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
    });

    if (!response.ok) throw new Error(`Failed to delete workout: ${response.status}`);

    console.log('Workout deleted:', workoutId);
  } catch (error) {
    console.error('Error deleting workout:', error);
    throw error;
  }
}

/**
 * Recent Workout History interfaces
 */
export interface RecentWorkoutExercise {
  exercise_name: string;
  sets_performed: number;
  reps_performed: number;
  duration_minutes?: number;
  calories_burned?: number;
  perceived_effort?: number;
}

export interface RecentWorkout {
  date: string;
  timestamp: string;
  exercise_count: number;
  total_exercises: number;
  exercises: RecentWorkoutExercise[];
}

export interface RecentWorkoutsResponse {
  success: boolean;
  recent_workouts: RecentWorkout[];
  count: number;
}

/**
 * Get recent workout sessions grouped by date
 */
export async function getRecentWorkouts(limit: number = 10, days: number = 30): Promise<RecentWorkoutsResponse> {
  try {
    const url = `${API_BASE_URL}/workout-logs/recent-workouts/?limit=${limit}&days=${days}`;
    
    const response = await fetch(url, {
      method: 'GET',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error('API Error Response:', errorText);
      throw new Error(`Failed to fetch recent workouts: ${response.status}`);
    }

    const data = await response.json();
    
    // Handle paginated response if needed
    if (data.results) {
      return {
        success: true,
        recent_workouts: data.results.recent_workouts || data.results,
        count: data.results.count || data.count || 0,
      };
    }
    
    return data;
  } catch (error) {
    console.error('Error fetching recent workouts:', error);
    throw error;
  }
}
