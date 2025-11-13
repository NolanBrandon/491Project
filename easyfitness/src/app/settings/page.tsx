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
  const [showOldPassword, setShowOldPassword] = useState(false);
  const [showNewPassword, setShowNewPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

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
      // Logout and redirect to login (logout handles "no active session" gracefully)
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

      <div className="flex-1 py-8 px-4 flex justify-center">
        <div className="w-full max-w-2xl flex flex-col items-center">
          <div className="mb-10 text-center">
            <h1 className="text-4xl font-bold mb-3">Account Settings</h1>
            <p className="text-lg text-gray-600">Manage your account information and preferences</p>
          </div>

          <div className="space-y-8 w-full max-w-3xl flex flex-col items-center">
          {/* Change Username Section */}
          <div className="auth-card w-full">
            <h2 className="text-2xl font-semibold mb-4 text-white">Change Username</h2>
            <p className="text-base text-white mb-6">Current username: <span className="font-medium">{user.username}</span></p>

            {usernameMessage && (
              <div className="mb-4 p-4 bg-transparent border border-green-200 text-white rounded-lg text-base">
                {usernameMessage}
              </div>
            )}
            {usernameError && (
              <div className="mb-4 p-4 bg-red-50 border border-red-200 text-white rounded-lg text-base">
                {usernameError}
              </div>
            )}

            <form onSubmit={handleUsernameChange} className="space-y-5">
              <div>
                <label htmlFor="newUsername" className="block text-base font-medium text-white mb-2">
                  New Username
                </label>
                <input
                  type="text"
                  id="newUsername"
                  className="auth-input text-base"
                  value={newUsername}
                  onChange={(e) => setNewUsername(e.target.value)}
                  required
                  minLength={3}
                  maxLength={50}
                  pattern="[a-zA-Z0-9_]+"
                  title="Username can only contain letters, numbers, and underscores"
                  disabled={usernameLoading}
                />
                <p className="mt-2 text-sm text-white">3-50 characters, letters, numbers, and underscores only</p>
              </div>

              <div>
                <label htmlFor="usernamePassword" className="block text-base font-medium text-white mb-2">
                  Current Password
                </label>
                <input
                  type="password"
                  id="usernamePassword"
                  className="auth-input text-base"
                  value={usernamePassword}
                  onChange={(e) => setUsernamePassword(e.target.value)}
                  required
                  disabled={usernameLoading}
                />
              </div>

              <button
                type="submit"
                className="auth-btn text-base px-6 py-3 rounded-lg"
                disabled={usernameLoading}
              >
                {usernameLoading ? 'Updating...' : 'Update Username'}
              </button>
            </form>
          </div>

          {/* Change Email Section */}
          <div className="auth-card w-full">
            <h2 className="text-2xl font-semibold mb-4 text-white">Change Email</h2>
            <p className="text-base text-white mb-6">Current email: <span className="font-medium">{user.email}</span></p>

            {emailMessage && (
              <div className="mb-4 p-4 bg-transparent border border-green-200 text-white rounded-lg text-base">
                {emailMessage}
              </div>
            )}
            {emailError && (
              <div className="mb-4 p-4 bg-red-50 border border-red-200 text-white rounded-lg text-base">
                {emailError}
              </div>
            )}

            <form onSubmit={handleEmailChange} className="space-y-5">
              <div>
                <label htmlFor="newEmail" className="block text-base font-medium text-white mb-2">
                  New Email
                </label>
                <input
                  type="email"
                  id="newEmail"
                  className="auth-input text-base"
                  value={newEmail}
                  onChange={(e) => setNewEmail(e.target.value)}
                  required
                  disabled={emailLoading}
                />
              </div>

              <div>
                <label htmlFor="emailPassword" className="block text-base font-medium text-white mb-2">
                  Current Password
                </label>
                <input
                  type="password"
                  id="emailPassword"
                  className="auth-input text-base"
                  value={emailPassword}
                  onChange={(e) => setEmailPassword(e.target.value)}
                  required
                  disabled={emailLoading}
                />
              </div>

              <button
                type="submit"
                className="auth-btn text-base px-6 py-3 rounded-lg"
                disabled={emailLoading}
              >
                {emailLoading ? 'Updating...' : 'Update Email'}
              </button>
            </form>
          </div>

          {/* Change Password Section */}
          <div className="auth-card w-full">
            <h2 className="text-2xl font-semibold mb-4 text-white">Change Password</h2>

            {passwordMessage && (
              <div className="mb-4 p-3 bg-transparent border border-green-200 text-white rounded-lg text-base">
                {passwordMessage}
              </div>
            )}
            {passwordError && (
              <div className="mb-4 p-3 bg-red-50 border border-red-200 text-white rounded-lg text-base">
                {passwordError}
              </div>
            )}

            <form onSubmit={handlePasswordChange} className="space-y-5">
              <div>
                <label htmlFor="oldPassword" className="block text-base font-medium text-white mb-2">
                  Current Password
                </label>
                <div className="relative">
                  <input
                    type={showOldPassword ? "text" : "password"}
                    id="oldPassword"
                    className="auth-input text-base w-full pr-12"
                    value={oldPassword}
                    onChange={(e) => setOldPassword(e.target.value)}
                    required
                    disabled={passwordLoading}
                  />
                  <button
                    type="button"
                    onClick={() => setShowOldPassword(!showOldPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700"
                    disabled={passwordLoading}
                  >
                    {showOldPassword ? (
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88" />
                      </svg>
                    ) : (
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
                        <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      </svg>
                    )}
                  </button>
                </div>
              </div>

              <div>
                <label htmlFor="newPassword" className="block text-base font-medium text-white mb-2">
                  New Password
                </label>
                <div className="relative">
                  <input
                    type={showNewPassword ? "text" : "password"}
                    id="newPassword"
                    className="auth-input text-base w-full pr-12"
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    required
                    minLength={8}
                    disabled={passwordLoading}
                  />
                  <button
                    type="button"
                    onClick={() => setShowNewPassword(!showNewPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700"
                    disabled={passwordLoading}
                  >
                    {showNewPassword ? (
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88" />
                      </svg>
                    ) : (
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
                        <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      </svg>
                    )}
                  </button>
                </div>
                <p className="mt-2 text-sm text-white">Minimum 8 characters</p>
              </div>

              <div>
                <label htmlFor="confirmPassword" className="block text-base font-medium text-white mb-2">
                  Confirm New Password
                </label>
                <div className="relative">
                  <input
                    type={showConfirmPassword ? "text" : "password"}
                    id="confirmPassword"
                    className="auth-input text-base w-full pr-12"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    required
                    minLength={8}
                    disabled={passwordLoading}
                  />
                  <button
                    type="button"
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700"
                    disabled={passwordLoading}
                  >
                    {showConfirmPassword ? (
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88" />
                      </svg>
                    ) : (
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
                        <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      </svg>
                    )}
                  </button>
                </div>
              </div>

              <button
                type="submit"
                className="auth-btn text-base px-6 py-3 rounded-lg"
                disabled={passwordLoading}
              >
                {passwordLoading ? 'Updating...' : 'Update Password'}
              </button>
            </form>
          </div>

          {/* Danger Zone - Delete Account */}
          <div className="auth-card border-2 border-red-200 w-full">
            <h2 className="text-2xl font-semibold mb-3 text-white">Danger Zone</h2>
            <p className="text-base text-white mb-6">
              Once you delete your account, there is no going back. This will permanently delete all your data including workouts, meal plans, and goals.
            </p>

            <button
              onClick={() => setShowDeleteModal(true)}
              className="px-6 py-3 bg-red-600 text-white text-base rounded-lg hover:bg-red-700 transition-colors font-medium"
            >
              Delete Account
            </button>
          </div>
          </div>
        </div>
      </div>

      {/* Delete Confirmation Modal */}
      {showDeleteModal && (
        <div className="fixed inset-0 bg-black/60 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full p-8">
            <h3 className="text-2xl font-bold mb-4 text-red-600">Delete Account</h3>

            <div className="mb-4 p-4 bg-red-50 border border-red-200 text-red-700 rounded-lg text-base">
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
              <div className="mb-4 p-4 bg-red-50 border border-red-200 text-red-700 rounded-lg text-base">
                {deleteError}
              </div>
            )}

            <div className="space-y-5">
              <div>
                <label htmlFor="deletePassword" className="block text-base font-medium text-gray-700 mb-2">
                  Enter your password to confirm
                </label>
                <input
                  type="password"
                  id="deletePassword"
                  className="w-full px-4 py-3 text-base text-black border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
                  value={deletePassword}
                  onChange={(e) => setDeletePassword(e.target.value)}
                  required
                  disabled={deleteLoading}
                />
              </div>

              <div>
                <label htmlFor="deleteConfirm" className="block text-base font-medium text-gray-700 mb-2">
                  Type <span className="font-bold">DELETE</span> to confirm
                </label>
                <input
                  type="text"
                  id="deleteConfirm"
                  className="w-full px-4 py-3 text-base text-black border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
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
                  className="flex-1 px-5 py-3 text-base border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors font-medium"
                  disabled={deleteLoading}
                >
                  Cancel
                </button>
                <button
                  onClick={handleDeleteAccount}
                  className="flex-1 px-5 py-3 text-base bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors font-medium disabled:opacity-50 disabled:cursor-not-allowed"
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
