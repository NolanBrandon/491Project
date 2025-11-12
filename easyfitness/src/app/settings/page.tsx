'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { useRouter } from 'next/navigation';
import Nav from '../components/navbar';
import Footer from '../components/footer';
import { changeUsername, changeEmail, changePassword, deleteAccount } from '@/lib/accountApi';

export default function SettingsPage() {
  const router = useRouter();
  const { user, isAuthenticated, loading: authLoading, refreshUser, logout } = useAuth();

  // Username form state
  const [newUsername, setNewUsername] = useState('');
  const [usernamePassword, setUsernamePassword] = useState('');
  const [usernameLoading, setUsernameLoading] = useState(false);
  const [usernameMessage, setUsernameMessage] = useState('');
  const [usernameError, setUsernameError] = useState('');

  // Email form state
  const [newEmail, setNewEmail] = useState('');
  const [emailPassword, setEmailPassword] = useState('');
  const [emailLoading, setEmailLoading] = useState(false);
  const [emailMessage, setEmailMessage] = useState('');
  const [emailError, setEmailError] = useState('');

  // Password form state
  const [oldPassword, setOldPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [passwordLoading, setPasswordLoading] = useState(false);
  const [passwordMessage, setPasswordMessage] = useState('');
  const [passwordError, setPasswordError] = useState('');

  // Delete account state
  const [deletePassword, setDeletePassword] = useState('');
  const [deleteConfirm, setDeleteConfirm] = useState('');
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [deleteLoading, setDeleteLoading] = useState(false);
  const [deleteError, setDeleteError] = useState('');

  // Redirect if not authenticated
  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.replace('/login');
    }
  }, [authLoading, isAuthenticated, router]);

  // Show loading while checking auth
  if (authLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  // Don't render if not authenticated
  if (!isAuthenticated || !user) {
    return null;
  }

  // Handle username change
  const handleUsernameChange = async (e: React.FormEvent) => {
    e.preventDefault();
    setUsernameLoading(true);
    setUsernameMessage('');
    setUsernameError('');

    try {
      const response = await changeUsername(user.id, newUsername, usernamePassword);
      setUsernameMessage(response.message);
      setNewUsername('');
      setUsernamePassword('');
      // Refresh user data to update navbar
      await refreshUser();
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to change username';
      setUsernameError(errorMessage);
    } finally {
      setUsernameLoading(false);
    }
  };

  // Handle email change
  const handleEmailChange = async (e: React.FormEvent) => {
    e.preventDefault();
    setEmailLoading(true);
    setEmailMessage('');
    setEmailError('');

    try {
      const response = await changeEmail(user.id, newEmail, emailPassword);
      setEmailMessage(response.message);
      setNewEmail('');
      setEmailPassword('');
      // Refresh user data
      await refreshUser();
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to change email';
      setEmailError(errorMessage);
    } finally {
      setEmailLoading(false);
    }
  };

  // Handle password change
  const handlePasswordChange = async (e: React.FormEvent) => {
    e.preventDefault();
    setPasswordLoading(true);
    setPasswordMessage('');
    setPasswordError('');

    // Validate passwords match
    if (newPassword !== confirmPassword) {
      setPasswordError('New passwords do not match');
      setPasswordLoading(false);
      return;
    }

    // Validate password length
    if (newPassword.length < 8) {
      setPasswordError('New password must be at least 8 characters');
      setPasswordLoading(false);
      return;
    }

    try {
      const response = await changePassword(user.id, oldPassword, newPassword);
      setPasswordMessage(response.message);
      setOldPassword('');
      setNewPassword('');
      setConfirmPassword('');
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to change password';
      setPasswordError(errorMessage);
    } finally {
      setPasswordLoading(false);
    }
  };

  // Handle account deletion
  const handleDeleteAccount = async () => {
    setDeleteLoading(true);
    setDeleteError('');

    try {
      await deleteAccount(user.id, deletePassword);
      // Logout and redirect to login
      await logout();
      router.replace('/login');
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to delete account';
      setDeleteError(errorMessage);
      setDeleteLoading(false);
    }
  };

  return (
    <div className="page-container blur-bg min-h-screen flex flex-col">
      <Nav />

      <div className="flex-1 px-4 py-8 max-w-4xl mx-auto w-full">
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Account Settings</h1>
          <p className="text-gray-600">Manage your account information and preferences</p>
        </div>

        <div className="space-y-6">
          {/* Change Username Section */}
          <div className="auth-card">
            <h2 className="text-xl font-semibold mb-4">Change Username</h2>
            <p className="text-sm text-gray-600 mb-4">Current username: <span className="font-medium">{user.username}</span></p>

            {usernameMessage && (
              <div className="mb-4 p-3 bg-green-50 border border-green-200 text-green-700 rounded-lg">
                {usernameMessage}
              </div>
            )}
            {usernameError && (
              <div className="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg">
                {usernameError}
              </div>
            )}

            <form onSubmit={handleUsernameChange} className="space-y-4">
              <div>
                <label htmlFor="newUsername" className="block text-sm font-medium text-gray-700 mb-1">
                  New Username
                </label>
                <input
                  type="text"
                  id="newUsername"
                  className="auth-input"
                  value={newUsername}
                  onChange={(e) => setNewUsername(e.target.value)}
                  required
                  minLength={3}
                  maxLength={50}
                  pattern="[a-zA-Z0-9_]+"
                  title="Username can only contain letters, numbers, and underscores"
                  disabled={usernameLoading}
                />
                <p className="mt-1 text-xs text-gray-500">3-50 characters, letters, numbers, and underscores only</p>
              </div>

              <div>
                <label htmlFor="usernamePassword" className="block text-sm font-medium text-gray-700 mb-1">
                  Current Password
                </label>
                <input
                  type="password"
                  id="usernamePassword"
                  className="auth-input"
                  value={usernamePassword}
                  onChange={(e) => setUsernamePassword(e.target.value)}
                  required
                  disabled={usernameLoading}
                />
              </div>

              <button
                type="submit"
                className="auth-btn"
                disabled={usernameLoading}
              >
                {usernameLoading ? 'Updating...' : 'Update Username'}
              </button>
            </form>
          </div>

          {/* Change Email Section */}
          <div className="auth-card">
            <h2 className="text-xl font-semibold mb-4">Change Email</h2>
            <p className="text-sm text-gray-600 mb-4">Current email: <span className="font-medium">{user.email}</span></p>

            {emailMessage && (
              <div className="mb-4 p-3 bg-green-50 border border-green-200 text-green-700 rounded-lg">
                {emailMessage}
              </div>
            )}
            {emailError && (
              <div className="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg">
                {emailError}
              </div>
            )}

            <form onSubmit={handleEmailChange} className="space-y-4">
              <div>
                <label htmlFor="newEmail" className="block text-sm font-medium text-gray-700 mb-1">
                  New Email
                </label>
                <input
                  type="email"
                  id="newEmail"
                  className="auth-input"
                  value={newEmail}
                  onChange={(e) => setNewEmail(e.target.value)}
                  required
                  disabled={emailLoading}
                />
              </div>

              <div>
                <label htmlFor="emailPassword" className="block text-sm font-medium text-gray-700 mb-1">
                  Current Password
                </label>
                <input
                  type="password"
                  id="emailPassword"
                  className="auth-input"
                  value={emailPassword}
                  onChange={(e) => setEmailPassword(e.target.value)}
                  required
                  disabled={emailLoading}
                />
              </div>

              <button
                type="submit"
                className="auth-btn"
                disabled={emailLoading}
              >
                {emailLoading ? 'Updating...' : 'Update Email'}
              </button>
            </form>
          </div>

          {/* Change Password Section */}
          <div className="auth-card">
            <h2 className="text-xl font-semibold mb-4">Change Password</h2>

            {passwordMessage && (
              <div className="mb-4 p-3 bg-green-50 border border-green-200 text-green-700 rounded-lg">
                {passwordMessage}
              </div>
            )}
            {passwordError && (
              <div className="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg">
                {passwordError}
              </div>
            )}

            <form onSubmit={handlePasswordChange} className="space-y-4">
              <div>
                <label htmlFor="oldPassword" className="block text-sm font-medium text-gray-700 mb-1">
                  Current Password
                </label>
                <input
                  type="password"
                  id="oldPassword"
                  className="auth-input"
                  value={oldPassword}
                  onChange={(e) => setOldPassword(e.target.value)}
                  required
                  disabled={passwordLoading}
                />
              </div>

              <div>
                <label htmlFor="newPassword" className="block text-sm font-medium text-gray-700 mb-1">
                  New Password
                </label>
                <input
                  type="password"
                  id="newPassword"
                  className="auth-input"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  required
                  minLength={8}
                  disabled={passwordLoading}
                />
                <p className="mt-1 text-xs text-gray-500">Minimum 8 characters</p>
              </div>

              <div>
                <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700 mb-1">
                  Confirm New Password
                </label>
                <input
                  type="password"
                  id="confirmPassword"
                  className="auth-input"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  required
                  minLength={8}
                  disabled={passwordLoading}
                />
              </div>

              <button
                type="submit"
                className="auth-btn"
                disabled={passwordLoading}
              >
                {passwordLoading ? 'Updating...' : 'Update Password'}
              </button>
            </form>
          </div>

          {/* Danger Zone - Delete Account */}
          <div className="auth-card border-2 border-red-200">
            <h2 className="text-xl font-semibold mb-2 text-red-600">Danger Zone</h2>
            <p className="text-sm text-gray-600 mb-4">
              Once you delete your account, there is no going back. This will permanently delete all your data including workouts, meal plans, and goals.
            </p>

            <button
              onClick={() => setShowDeleteModal(true)}
              className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors font-medium"
            >
              Delete Account
            </button>
          </div>
        </div>
      </div>

      {/* Delete Confirmation Modal */}
      {showDeleteModal && (
        <div className="fixed inset-0 bg-black/60 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
            <h3 className="text-xl font-bold mb-4 text-red-600">Delete Account</h3>

            <div className="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
              <p className="font-semibold mb-2">⚠️ This action cannot be undone!</p>
              <p>All your data will be permanently deleted, including:</p>
              <ul className="list-disc list-inside mt-2 space-y-1">
                <li>Workout plans and logs</li>
                <li>Meal plans and nutrition logs</li>
                <li>Goals and metrics</li>
                <li>Account information</li>
              </ul>
            </div>

            {deleteError && (
              <div className="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
                {deleteError}
              </div>
            )}

            <div className="space-y-4">
              <div>
                <label htmlFor="deletePassword" className="block text-sm font-medium text-gray-700 mb-1">
                  Enter your password to confirm
                </label>
                <input
                  type="password"
                  id="deletePassword"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
                  value={deletePassword}
                  onChange={(e) => setDeletePassword(e.target.value)}
                  required
                  disabled={deleteLoading}
                />
              </div>

              <div>
                <label htmlFor="deleteConfirm" className="block text-sm font-medium text-gray-700 mb-1">
                  Type <span className="font-bold">DELETE</span> to confirm
                </label>
                <input
                  type="text"
                  id="deleteConfirm"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
                  value={deleteConfirm}
                  onChange={(e) => setDeleteConfirm(e.target.value)}
                  required
                  disabled={deleteLoading}
                  placeholder="Type DELETE"
                />
              </div>

              <div className="flex gap-3 pt-2">
                <button
                  onClick={() => {
                    setShowDeleteModal(false);
                    setDeletePassword('');
                    setDeleteConfirm('');
                    setDeleteError('');
                  }}
                  className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors font-medium"
                  disabled={deleteLoading}
                >
                  Cancel
                </button>
                <button
                  onClick={handleDeleteAccount}
                  className="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors font-medium disabled:opacity-50 disabled:cursor-not-allowed"
                  disabled={deleteLoading || deleteConfirm !== 'DELETE' || !deletePassword}
                >
                  {deleteLoading ? 'Deleting...' : 'Delete Forever'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      <Footer />
    </div>
  );
}
