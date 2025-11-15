const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api';

export interface NutritionLog {
  id: string;
  user: string;
  date_eaten: string;
  meal_type: string;
  food_name: string;
  quantity: number;
  calories: number | null;
  created_at: string;
  updated_at: string;
  protein?: number;
}

export interface CreateNutritionLogData {
  date_eaten: string;
  meal_type: string;
  food_name: string;
  quantity: number;
  calories?: number;
  user?: string;
  protein?: number;
}

/**
 * Get all nutrition logs for the authenticated user
 */
export async function getNutritionLogs(): Promise<NutritionLog[]> {
  try {
    const response = await fetch(`${API_BASE_URL}/nutrition-logs/`, {
      method: 'GET',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
    });
    if (!response.ok) throw new Error(`Failed to fetch nutrition logs: ${response.status}`);
    const data = await response.json();
    return data.results || data;
  } catch (err) {
    console.error('Error fetching nutrition logs:', err);
    throw err;
  }
}

/**
 * Get a single nutrition log by ID
 */
export async function getNutritionLog(id: string): Promise<NutritionLog> {
  try {
    const response = await fetch(`${API_BASE_URL}/nutrition-logs/${id}/`, {
      method: 'GET',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
    });
    if (!response.ok) throw new Error(`Failed to fetch nutrition log: ${response.status}`);
    return response.json();
  } catch (err) {
    console.error(`Error fetching nutrition log ${id}:`, err);
    throw err;
  }
}

/**
 * Create a new nutrition log
 */
export async function createNutritionLog(data: CreateNutritionLogData): Promise<NutritionLog> {
  try {
    const response = await fetch(`${API_BASE_URL}/nutrition-logs/`, {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      const errData = await response.json();
      throw new Error(`Failed to create nutrition log: ${JSON.stringify(errData)}`);
    }
    return response.json();
  } catch (err) {
    console.error('Error creating nutrition log:', err);
    throw err;
  }
}

/**
 * Update an existing nutrition log
 */
export async function updateNutritionLog(
  id: string,
  data: Partial<CreateNutritionLogData>
): Promise<NutritionLog> {
  try {
    const response = await fetch(`${API_BASE_URL}/nutrition-logs/${id}/`, {
      method: 'PATCH',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      const errData = await response.json();
      throw new Error(`Failed to update nutrition log: ${JSON.stringify(errData)}`);
    }
    return response.json();
  } catch (err) {
    console.error(`Error updating nutrition log ${id}:`, err);
    throw err;
  }
}

/**
 * Delete a nutrition log
 */
export async function deleteNutritionLog(id: string): Promise<void> {
  try {
    const response = await fetch(`${API_BASE_URL}/nutrition-logs/${id}/`, {
      method: 'DELETE',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
    });
    if (!response.ok) throw new Error(`Failed to delete nutrition log: ${response.status}`);
    console.log(`Nutrition log ${id} deleted successfully`);
  } catch (err) {
    console.error(`Error deleting nutrition log ${id}:`, err);
    throw err;
  }
}
