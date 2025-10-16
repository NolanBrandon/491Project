/**
 * Goals API Service
 * Handles all API calls related to user goals
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// TypeScript interfaces
export interface Goal {
  id: string;
  user: string;
  title: string;
  description: string;
  goal_type: string;
  target_weight_kg: number | null;
  target_date: string | null;
  start_date: string | null;
  end_date: string | null;
  status: 'active' | 'completed' | 'paused';
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface CreateGoalData {
  title: string;
  description?: string;
  goal_type?: string;
  target_weight_kg?: number;
  target_date?: string;
  start_date?: string;
  end_date?: string;
  status?: 'active' | 'completed' | 'paused';
}

export interface UpdateGoalData {
  title?: string;
  description?: string;
  goal_type?: string;
  target_weight_kg?: number;
  target_date?: string;
  start_date?: string;
  end_date?: string;
  status?: 'active' | 'completed' | 'paused';
  is_active?: boolean;
}

/**
 * Get all goals for the authenticated user
 */
export async function getGoals(): Promise<Goal[]> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/goals/`, {
      method: 'GET',
      credentials: 'include', // Important for session cookies
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch goals: ${response.status}`);
    }

    const data = await response.json();
    console.log('Goals fetched:', data);
    return data.results || data; // Handle paginated or direct response
  } catch (error) {
    console.error('Error fetching goals:', error);
    throw error;
  }
}

/**
 * Get a specific goal by ID
 */
export async function getGoal(goalId: string): Promise<Goal> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/goals/${goalId}/`, {
      method: 'GET',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch goal: ${response.status}`);
    }

    const data = await response.json();
    console.log('Goal fetched:', data);
    return data;
  } catch (error) {
    console.error('Error fetching goal:', error);
    throw error;
  }
}

/**
 * Create a new goal
 */
export async function createGoal(goalData: CreateGoalData): Promise<Goal> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/goals/`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(goalData),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(`Failed to create goal: ${JSON.stringify(errorData)}`);
    }

    const data = await response.json();
    console.log('Goal created:', data);
    return data;
  } catch (error) {
    console.error('Error creating goal:', error);
    throw error;
  }
}

/**
 * Update an existing goal
 */
export async function updateGoal(goalId: string, goalData: UpdateGoalData): Promise<Goal> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/goals/${goalId}/`, {
      method: 'PATCH',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(goalData),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(`Failed to update goal: ${JSON.stringify(errorData)}`);
    }

    const data = await response.json();
    console.log('Goal updated:', data);
    return data;
  } catch (error) {
    console.error('Error updating goal:', error);
    throw error;
  }
}

/**
 * Delete a goal
 */
export async function deleteGoal(goalId: string): Promise<void> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/goals/${goalId}/`, {
      method: 'DELETE',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`Failed to delete goal: ${response.status}`);
    }

    console.log('Goal deleted:', goalId);
  } catch (error) {
    console.error('Error deleting goal:', error);
    throw error;
  }
}
