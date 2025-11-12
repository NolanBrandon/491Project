/**
 * Account management API service for Django backend
 * Handles username, email, password changes and account deletion
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api';

interface ChangeUsernameResponse {
  message: string;
  username: string;
}

interface ChangeEmailResponse {
  message: string;
  email: string;
}

interface ChangePasswordResponse {
  message: string;
}

interface DeleteAccountResponse {
  message: string;
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
    credentials: 'include', // Essential for session cookies
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  };

  return fetch(url, config);
}

/**
 * Parse Django REST Framework error responses
 */
function parseErrorResponse(errorData: any): string {
  // Handle field-specific errors
  if (typeof errorData === 'object' && !errorData.error) {
    const errorMessages: string[] = [];

    for (const [field, messages] of Object.entries(errorData)) {
      if (Array.isArray(messages)) {
        // Format field name nicely
        const fieldName = field === 'non_field_errors' ? '' :
                         field.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()) + ': ';
        messages.forEach(msg => errorMessages.push(fieldName + msg));
      } else if (typeof messages === 'string') {
        const fieldName = field === 'non_field_errors' ? '' :
                         field.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()) + ': ';
        errorMessages.push(fieldName + messages);
      }
    }

    return errorMessages.join('; ') || 'Operation failed';
  }

  // Fallback to simple error message
  return errorData.error || errorData.message || 'Operation failed';
}

/**
 * Change user's username
 */
export async function changeUsername(
  userId: string,
  newUsername: string,
  currentPassword: string
): Promise<ChangeUsernameResponse> {
  const response = await fetchWithCredentials(`/users/${userId}/change_username/`, {
    method: 'POST',
    body: JSON.stringify({
      new_username: newUsername,
      current_password: currentPassword,
    }),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(parseErrorResponse(errorData));
  }

  return response.json();
}

/**
 * Change user's email
 */
export async function changeEmail(
  userId: string,
  newEmail: string,
  currentPassword: string
): Promise<ChangeEmailResponse> {
  const response = await fetchWithCredentials(`/users/${userId}/change_email/`, {
    method: 'POST',
    body: JSON.stringify({
      new_email: newEmail,
      current_password: currentPassword,
    }),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(parseErrorResponse(errorData));
  }

  return response.json();
}

/**
 * Change user's password
 */
export async function changePassword(
  userId: string,
  oldPassword: string,
  newPassword: string
): Promise<ChangePasswordResponse> {
  const response = await fetchWithCredentials(`/users/${userId}/change_password/`, {
    method: 'POST',
    body: JSON.stringify({
      old_password: oldPassword,
      new_password: newPassword,
    }),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(parseErrorResponse(errorData));
  }

  return response.json();
}

/**
 * Delete user account permanently
 * This action is irreversible and will cascade delete all related data
 */
export async function deleteAccount(
  userId: string,
  currentPassword: string
): Promise<DeleteAccountResponse> {
  const response = await fetchWithCredentials(`/users/${userId}/`, {
    method: 'DELETE',
    body: JSON.stringify({
      current_password: currentPassword,
      confirm_deletion: true,
    }),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(parseErrorResponse(errorData));
  }

  // DELETE returns 204 No Content, so parse as text first
  const text = await response.text();
  return text ? JSON.parse(text) : { message: 'Account deleted successfully' };
}
