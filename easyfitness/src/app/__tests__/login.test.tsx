import { render, screen } from '@testing-library/react';
import LoginPage from '../login/page';

// Mock Next.js navigation
jest.mock('next/navigation', () => ({
  useRouter: () => ({
    push: jest.fn(),
    replace: jest.fn(),
    prefetch: jest.fn(),
  }),
  usePathname: () => '/',
  useSearchParams: () => new URLSearchParams(),
}));

// Mock fetch
beforeAll(() => {
  global.fetch = jest.fn(() =>
    Promise.resolve({
      json: () => Promise.resolve({ status: 'ok' }),
    })
  ) as jest.Mock;
});

afterAll(() => {
  jest.restoreAllMocks();
});

describe('Login Page', () => {
  it('renders login heading', () => {
    render(<LoginPage />);
    expect(screen.getByRole('heading', { name: /sign in/i })).toBeInTheDocument();
  });

  it('allows user to input email and password', () => {
    render(<LoginPage />);
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
  });
});
