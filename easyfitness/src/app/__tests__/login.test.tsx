import { render, screen, fireEvent } from '@testing-library/react';
import LoginPage from '../login/page';

describe('Login Page', () => {
  it('renders login heading', () => {
    render(<LoginPage />);
    expect(screen.getByRole('heading', { name: /sign in to your account/i })).toBeInTheDocument();
  });

  it('allows typing email and password', () => {
    render(<LoginPage />);
    fireEvent.change(screen.getByPlaceholderText(/email address/i), { target: { value: 'test@example.com' } });
    fireEvent.change(screen.getByPlaceholderText(/password/i), { target: { value: 'secret' } });
    expect(screen.getByDisplayValue('test@example.com')).toBeInTheDocument();
    expect(screen.getByDisplayValue('secret')).toBeInTheDocument();
  });
});
