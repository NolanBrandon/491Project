// src/app/__tests__/nutrition.test.tsx
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import NutritionPage from '../Nutrition/page';
import React, { createContext } from 'react';

// ----------------------------------------------------
// Mock router
// ----------------------------------------------------
const mockPush = jest.fn();
const mockReplace = jest.fn();
jest.mock('next/navigation', () => ({
  useRouter: () => ({
    push: mockPush,
    replace: mockReplace,
  }),
}));

// ----------------------------------------------------
// Mock API
// ----------------------------------------------------
jest.mock('@/lib/nutritionApi', () => {
  const mockLogs = [
    {
      id: '1',
      food_name: 'Chicken Breast',
      meal_type: 'lunch',
      date_eaten: '2025-01-01T12:00:00Z',
      calories: 350,
      protein: 40,
    },
    {
      id: '2',
      food_name: 'Oatmeal',
      meal_type: 'breakfast',
      date_eaten: '2025-01-01T08:00:00Z',
      calories: 250,
      protein: 10,
    },
  ];

  return {
    getNutritionLogs: jest.fn().mockResolvedValue(mockLogs),
    deleteNutritionLog: jest.fn().mockResolvedValue(undefined),
  };
});

// ----------------------------------------------------
// Mock Auth Context
// ----------------------------------------------------
const AuthContext = createContext({
  user: { id: '123', username: 'testuser', email: 'test@example.com' },
  loading: false,
  isAuthenticated: true,
  login: jest.fn(),
  logout: jest.fn(),
  register: jest.fn(),
  refreshUser: jest.fn(),
});

function TestAuthProvider({ children }: { children: React.ReactNode }) {
  return <AuthContext.Provider value={{
    user: { id: '123', username: 'testuser', email: 'test@example.com' },
    loading: false,
    isAuthenticated: true,
    login: jest.fn(),
    logout: jest.fn(),
    register: jest.fn(),
    refreshUser: jest.fn(),
  }}>{children}</AuthContext.Provider>;
}

// Patch useAuth hook to use our mock context
jest.mock('@/contexts/AuthContext', () => ({
  useAuth: () => React.useContext(AuthContext),
}));

// ----------------------------------------------------
// Helper render
// ----------------------------------------------------
const renderWithAuth = (ui: React.ReactNode) => render(<TestAuthProvider>{ui}</TestAuthProvider>);

// ----------------------------------------------------
// Tests
// ----------------------------------------------------
describe('Nutrition Page', () => {
  it('renders the Nutrition Logs heading', async () => {
    renderWithAuth(<NutritionPage />);
    expect(await screen.findByText(/Nutrition Logs/i)).toBeInTheDocument();
  });

  it('renders a list of nutrition logs from the API', async () => {
    renderWithAuth(<NutritionPage />);
    expect(await screen.findByText(/Chicken Breast/i)).toBeInTheDocument();
    expect(screen.getByText(/lunch/i)).toBeInTheDocument();
    expect(screen.getByText(/350 calories/i)).toBeInTheDocument();
    expect(screen.getByText(/40 g protein/i)).toBeInTheDocument();
  });

  it('shows delete buttons for each log', async () => {
    renderWithAuth(<NutritionPage />);
    const deleteButtons = await screen.findAllByText(/delete/i);
    expect(deleteButtons.length).toBe(2);
  });
});
