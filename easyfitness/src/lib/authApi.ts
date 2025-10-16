/**
 * Authentication API service for Django backend
 * Handles session-based authentication with HTTP-only cookies
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api';

interface User {
  id: string;
  username: string;
  email: string;
  gender?: string;
  date_of_birth?: string;
  last_login_date?: string;
  login_streak?: number;
  created_at?: string;
}

interface LoginResponse {
  message: string;
  user: User;
}

interface SessionResponse {
  authenticated: boolean;
  user: User;
}

interface ValidationResponse {
  valid: boolean;
  user_id?: string;
}

interface RegisterData {
  username: string;
  email: string;
  password: string;
  password_confirm: string;
  gender?: string;
  date_of_birth?: string;
}

/**
 * Base fetch wrapper with credentials support for cookies
 */
async function fetchWithCredentials(
  endpoint: string,
  options: RequestInit = {}
): Promise<Response> {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const config: RequestInit = {
    ...options,
    credentials: 'include', // Essential for cookies
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  };
  
  return fetch(url, config);
}

/**
 * Register a new user and auto-login
 */
export async function register(data: RegisterData): Promise<LoginResponse> {
  const response = await fetchWithCredentials('/users/', {
    method: 'POST',
    body: JSON.stringify(data),
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || 'Registration failed');
  }
  
  return response.json();
}

/**
 * Login with username and password
 */
export async function login(username: string, password: string): Promise<LoginResponse> {
  const response = await fetchWithCredentials('/users/login/', {
    method: 'POST',
    body: JSON.stringify({ username, password }),
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || 'Login failed');
  }
  
  return response.json();
}

/**
 * Logout and clear session
 */
export async function logout(): Promise<void> {
  const response = await fetchWithCredentials('/users/logout/', {
    method: 'POST',
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || 'Logout failed');
  }
}

/**
 * Get current session user
 */
export async function getSessionUser(): Promise<User | null> {
  try {
    const response = await fetchWithCredentials('/users/session/');
    
    if (!response.ok) {
      return null;
    }
    
    const data: SessionResponse = await response.json();
    return data.authenticated ? data.user : null;
  } catch (error) {
    console.error('Error fetching session user:', error);
    return null;
  }
}

/**
 * Validate current session (lightweight check)
 */
export async function validateSession(): Promise<boolean> {
  try {
    const response = await fetchWithCredentials('/users/validate_session/');
    
    if (!response.ok) {
      return false;
    }
    
    const data: ValidationResponse = await response.json();
    return data.valid;
  } catch (error) {
    console.error('Error validating session:', error);
    return false;
  }
}

/**
 * Export the base fetch function for other API calls
 */
export { fetchWithCredentials };
