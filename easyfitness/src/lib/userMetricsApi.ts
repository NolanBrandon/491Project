// API functions for user metrics

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api';

export interface UserMetrics {
  id: string;
  user: string;
  date_recorded: string;
  weight_kg?: number;
  height_cm?: number;
  activity_level?: string;
}

export interface CreateUserMetricsData {
  date_recorded: string;
  weight_kg?: number;
  height_cm?: number;
  activity_level?: string;
}

// Get all user metrics
export async function getUserMetrics(): Promise<UserMetrics[]> {
  const response = await fetch(`${API_BASE_URL}/user-metrics/`, {
    method: 'GET',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch user metrics: ${response.status}`);
  }

  const data = await response.json();

  // Django REST framework returns paginated data with 'results' key
  return Array.isArray(data) ? data : (data.results || []);
}

// Get latest user metrics
export async function getLatestUserMetrics(): Promise<UserMetrics | null> {
  const metrics = await getUserMetrics();
  if (!Array.isArray(metrics) || metrics.length === 0) return null;

  // Sort by date_recorded descending and return the first one
  const sorted = metrics.sort((a, b) =>
    new Date(b.date_recorded).getTime() - new Date(a.date_recorded).getTime()
  );

  return sorted[0];
}

// Create new user metrics
export async function createUserMetrics(data: CreateUserMetricsData): Promise<UserMetrics> {
  const response = await fetch(`${API_BASE_URL}/user-metrics/`, {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || `Failed to create user metrics: ${response.status}`);
  }

  return response.json();
}

// Update user metrics
export async function updateUserMetrics(id: string, data: Partial<CreateUserMetricsData>): Promise<UserMetrics> {
  const response = await fetch(`${API_BASE_URL}/user-metrics/${id}/`, {
    method: 'PATCH',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || `Failed to update user metrics: ${response.status}`);
  }

  return response.json();
}

// Delete user metrics
export async function deleteUserMetrics(id: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/user-metrics/${id}/`, {
    method: 'DELETE',
    credentials: 'include',
  });

  if (!response.ok) {
    throw new Error(`Failed to delete user metrics: ${response.status}`);
  }
}
