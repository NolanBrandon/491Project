import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import SettingsPage from '../settings/page';
import * as accountApi from '@/lib/accountApi';

// Mock Next.js navigation
jest.mock('next/navigation', () => ({
  useRouter: () => ({
    push: jest.fn(),
    replace: jest.fn(),
    prefetch: jest.fn(),
  }),
  usePathname: () => '/settings',
  useSearchParams: () => new URLSearchParams(),
}));

// Mock AuthContext
jest.mock('@/contexts/AuthContext', () => ({
  useAuth: () => ({
    user: {
      id: '123',
      username: 'testuser',
      email: 'test@example.com',
    },
    isAuthenticated: true,
    loading: false,
    refreshUser: jest.fn(),
    logout: jest.fn(),
  }),
}));

// Mock account API
jest.mock('@/lib/accountApi');

describe('Settings Page', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders all account settings sections', () => {
    render(<SettingsPage />);

    expect(screen.getByText('Account Settings')).toBeInTheDocument();
    expect(screen.getByText('Change Username')).toBeInTheDocument();
    expect(screen.getByText('Change Email')).toBeInTheDocument();
    expect(screen.getByText('Change Password')).toBeInTheDocument();
    expect(screen.getByText('Danger Zone')).toBeInTheDocument();
  });

  it('displays current username and email', () => {
    render(<SettingsPage />);

    expect(screen.getByText(/Current username:/)).toBeInTheDocument();
    expect(screen.getByText('testuser')).toBeInTheDocument();
    expect(screen.getByText(/Current email:/)).toBeInTheDocument();
    expect(screen.getByText('test@example.com')).toBeInTheDocument();
  });

  it('has username change form with required fields', () => {
    render(<SettingsPage />);

    const newUsernameInput = screen.getByLabelText('New Username');
    const usernamePasswordInput = screen.getAllByLabelText('Current Password')[0];

    expect(newUsernameInput).toBeInTheDocument();
    expect(usernamePasswordInput).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Update Username/i })).toBeInTheDocument();
  });

  it('has email change form with required fields', () => {
    render(<SettingsPage />);

    const newEmailInput = screen.getByLabelText('New Email');
    const emailPasswordInput = screen.getAllByLabelText('Current Password')[1];

    expect(newEmailInput).toBeInTheDocument();
    expect(emailPasswordInput).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Update Email/i })).toBeInTheDocument();
  });

  it('has password change form with all fields', () => {
    render(<SettingsPage />);

    expect(screen.getAllByLabelText('Current Password')[2]).toBeInTheDocument();
    expect(screen.getByLabelText('New Password')).toBeInTheDocument();
    expect(screen.getByLabelText('Confirm New Password')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Update Password/i })).toBeInTheDocument();
  });

  it('has delete account button', () => {
    render(<SettingsPage />);

    expect(screen.getByRole('button', { name: /Delete Account/i })).toBeInTheDocument();
  });

  it('validates username input pattern', () => {
    render(<SettingsPage />);

    const newUsernameInput = screen.getByLabelText('New Username') as HTMLInputElement;

    expect(newUsernameInput).toHaveAttribute('pattern', '[a-zA-Z0-9_]+');
    expect(newUsernameInput).toHaveAttribute('minlength', '3');
    expect(newUsernameInput).toHaveAttribute('maxlength', '50');
  });

  it('validates password minimum length', () => {
    render(<SettingsPage />);

    const newPasswordInput = screen.getByLabelText('New Password') as HTMLInputElement;

    expect(newPasswordInput).toHaveAttribute('minlength', '8');
  });

  it('shows delete confirmation modal when delete button is clicked', () => {
    render(<SettingsPage />);

    const deleteButton = screen.getByRole('button', { name: /Delete Account/i });
    fireEvent.click(deleteButton);

    expect(screen.getByText(/This action cannot be undone!/)).toBeInTheDocument();
    expect(screen.getByText(/Type DELETE to confirm/)).toBeInTheDocument();
  });

  it('closes delete modal when cancel is clicked', () => {
    render(<SettingsPage />);

    // Open modal
    const deleteButton = screen.getByRole('button', { name: /Delete Account/i });
    fireEvent.click(deleteButton);

    // Close modal
    const cancelButton = screen.getByRole('button', { name: /Cancel/i });
    fireEvent.click(cancelButton);

    expect(screen.queryByText(/This action cannot be undone!/)).not.toBeInTheDocument();
  });

  it('disables delete forever button until requirements are met', () => {
    render(<SettingsPage />);

    // Open modal
    const deleteButton = screen.getByRole('button', { name: /Delete Account/i });
    fireEvent.click(deleteButton);

    const deleteForeverButton = screen.getByRole('button', { name: /Delete Forever/i });

    // Should be disabled initially
    expect(deleteForeverButton).toBeDisabled();

    // Enter password
    const passwordInput = screen.getByLabelText(/Enter your password to confirm/i);
    fireEvent.change(passwordInput, { target: { value: 'testpassword' } });

    // Should still be disabled without typing DELETE
    expect(deleteForeverButton).toBeDisabled();

    // Type DELETE
    const deleteConfirmInput = screen.getByPlaceholderText('Type DELETE');
    fireEvent.change(deleteConfirmInput, { target: { value: 'DELETE' } });

    // Now should be enabled
    expect(deleteForeverButton).not.toBeDisabled();
  });

  it('displays helper text for username requirements', () => {
    render(<SettingsPage />);

    expect(screen.getByText(/3-50 characters, letters, numbers, and underscores only/)).toBeInTheDocument();
  });

  it('displays helper text for password requirements', () => {
    render(<SettingsPage />);

    expect(screen.getByText(/Minimum 8 characters/)).toBeInTheDocument();
  });

  it('lists what will be deleted in confirmation modal', () => {
    render(<SettingsPage />);

    const deleteButton = screen.getByRole('button', { name: /Delete Account/i });
    fireEvent.click(deleteButton);

    expect(screen.getByText(/Workout plans and logs/)).toBeInTheDocument();
    expect(screen.getByText(/Meal plans and nutrition logs/)).toBeInTheDocument();
    expect(screen.getByText(/Goals and metrics/)).toBeInTheDocument();
    expect(screen.getByText(/Account information/)).toBeInTheDocument();
  });
});
