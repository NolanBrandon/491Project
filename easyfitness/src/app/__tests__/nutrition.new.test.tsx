/**
 * src/app/__tests__/nutrition.new.test.tsx
 *
 * Tests the "Add Nutrition Log" form behavior.
 */

import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import '@testing-library/jest-dom';
import NewNutritionLogPage from '../Nutrition/new/page';

// Mocks (mirror previous file)
jest.mock('@/contexts/AuthContext', () => ({
  useAuth: () => ({
    user: { id: 'user-1', username: 'testuser', email: 't@example.com' },
    loading: false,
    isAuthenticated: true,
  }),
}));

const createNutritionLogMock = jest.fn().mockResolvedValue({
  id: 'new-log',
  user: 'user-1',
  date_eaten: new Date().toISOString(),
  meal_type: 'breakfast',
  food_name: 'Test Food',
  quantity: 0,
  calories: 123,
});

jest.mock('@/lib/nutritionApi', () => ({
  createNutritionLog: (...args: any[]) => createNutritionLogMock(...args),
}));

const pushMock = jest.fn();
jest.mock('next/navigation', () => ({
  useRouter: () => ({ push: pushMock, replace: jest.fn() }),
}));

describe('NewNutritionLogPage', () => {
  beforeEach(() => {
    createNutritionLogMock.mockClear();
    pushMock.mockClear();
  });

  it('renders form and submits new log', async () => {
    render(<NewNutritionLogPage />);

    // verify inputs present
    const foodInput = screen.getByLabelText(/food name/i);
    const mealSelect = screen.getByLabelText(/meal type/i);
    const caloriesInput = screen.getByLabelText(/calories/i);
    const dateInput = screen.getByLabelText(/date eaten/i);
    const timeInput = screen.getByLabelText(/time eaten/i);
    const submitBtn = screen.getByRole('button', { name: /add log/i });

    await userEvent.type(foodInput, 'Test Food');
    await userEvent.selectOptions(mealSelect, 'breakfast');
    await userEvent.type(caloriesInput, '123');
    await userEvent.type(dateInput, '2025-11-14');
    await userEvent.type(timeInput, '07:23');

    await userEvent.click(submitBtn);

    await waitFor(() => {
      expect(createNutritionLogMock).toHaveBeenCalled();
    });

    // expect redirect to dashboard
    expect(pushMock).toHaveBeenCalledWith('/dashboard');
  });
});
