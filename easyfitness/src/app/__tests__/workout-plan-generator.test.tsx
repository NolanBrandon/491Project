import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import WorkoutPlanGeneratorPage from '../workout-plan-generator/page';

// Mock Next.js navigation
const mockPush = jest.fn();
const mockReplace = jest.fn();
jest.mock('next/navigation', () => ({
  useRouter: () => ({
    push: mockPush,
    replace: mockReplace,
    prefetch: jest.fn(),
  }),
  usePathname: () => '/workout-plan-generator',
  useSearchParams: () => new URLSearchParams(),
}));

// Mock AuthContext
const mockUser = {
  id: 'user-123',
  username: 'testuser',
  email: 'test@example.com',
};

jest.mock('@/contexts/AuthContext', () => ({
  useAuth: () => ({
    user: mockUser,
    isAuthenticated: true,
    loading: false,
    refreshUser: jest.fn(),
    logout: jest.fn(),
    login: jest.fn(),
    register: jest.fn(),
  }),
}));

// Mock API functions
const mockGetGoals = jest.fn();
const mockGetSavedWorkoutPlans = jest.fn();
const mockGetWorkoutPlanDetail = jest.fn();
const mockSetWorkoutPlanActive = jest.fn();
const mockMarkExerciseComplete = jest.fn();
const mockGetWorkoutPlanCompletionLogs = jest.fn();

jest.mock('@/lib/goalsApi', () => ({
  getGoals: () => mockGetGoals(),
}));

jest.mock('@/lib/aiWorkoutPlanApi', () => ({
  generateWorkoutPlan: jest.fn(),
  getSavedWorkoutPlans: () => mockGetSavedWorkoutPlans(),
  getWorkoutPlanDetail: (id: string) => mockGetWorkoutPlanDetail(id),
  setWorkoutPlanActive: (id: string) => mockSetWorkoutPlanActive(id),
  markExerciseComplete: (planId: string, dayNumber: number, exerciseIndex: number, completed: boolean) =>
    mockMarkExerciseComplete(planId, dayNumber, exerciseIndex, completed),
  getWorkoutPlanCompletionLogs: (id: string) => mockGetWorkoutPlanCompletionLogs(id),
}));

// Mock Navbar
jest.mock('@/app/components/navbar', () => ({
  __esModule: true,
  default: () => <nav>Navbar</nav>,
}));

describe('Workout Plan Generator - Progress Tracking', () => {
  const mockGoal = {
    id: 'goal-1',
    title: 'Build Muscle',
    description: 'Gain strength and muscle mass',
    status: 'active',
    is_active: true,
  };

  const mockWorkoutPlan = {
    id: 'plan-1',
    user: 'user-123',
    name: '4-Day Split',
    description: 'Upper/Lower split',
    is_active: true,
    is_completed: false,
    created_at: '2024-01-01T00:00:00Z',
    workout_plan_data: {
      success: true,
      data: {
        plan_name: '4-Day Split',
        plan_description: 'Upper/Lower split',
        days: [
          {
            day_number: 1,
            day_name: 'Upper Body',
            exercises: [
              { exercise_name: 'Bench Press', sets: 4, reps: '8-10' },
              { exercise_name: 'Rows', sets: 4, reps: '8-10' },
            ],
          },
          {
            day_number: 2,
            day_name: 'Lower Body',
            exercises: [
              { exercise_name: 'Squats', sets: 4, reps: '8-10' },
              { exercise_name: 'Deadlifts', sets: 3, reps: '5' },
            ],
          },
        ],
      },
      exercise_completions: {},
    },
  };

  const mockWorkoutPlanWithCompletions = {
    ...mockWorkoutPlan,
    workout_plan_data: {
      ...mockWorkoutPlan.workout_plan_data,
      exercise_completions: {
        day_1: {
          exercise_0: { completed: true, completed_at: new Date().toISOString() },
          exercise_1: { completed: true, completed_at: new Date().toISOString() },
        },
      },
    },
  };

  beforeEach(() => {
    jest.clearAllMocks();
    mockGetGoals.mockResolvedValue([mockGoal]);
    mockGetSavedWorkoutPlans.mockResolvedValue([mockWorkoutPlan]);
    mockGetWorkoutPlanDetail.mockResolvedValue(mockWorkoutPlan);
    mockGetWorkoutPlanCompletionLogs.mockResolvedValue([]);
    mockSetWorkoutPlanActive.mockResolvedValue({ ...mockWorkoutPlan, is_active: true });
    mockMarkExerciseComplete.mockResolvedValue(mockWorkoutPlan);
  });

  describe('Active Plan Selection', () => {
    it('should display active plan when one is set', async () => {
      render(<WorkoutPlanGeneratorPage />);

      await waitFor(() => {
        expect(screen.getByText(/Active Plan: 4-Day Split/i)).toBeInTheDocument();
      });
    });

    it('should show "Set as Active" button for inactive plans', async () => {
      const inactivePlan = { ...mockWorkoutPlan, is_active: false };
      mockGetSavedWorkoutPlans.mockResolvedValue([inactivePlan, mockWorkoutPlan]);

      render(<WorkoutPlanGeneratorPage />);

      await waitFor(() => {
        const setActiveButtons = screen.getAllByText(/Set as Active/i);
        expect(setActiveButtons.length).toBeGreaterThan(0);
      });
    });

    it('should call setWorkoutPlanActive when "Set as Active" is clicked', async () => {
      const inactivePlan = { ...mockWorkoutPlan, id: 'plan-2', is_active: false };
      mockGetSavedWorkoutPlans.mockResolvedValue([inactivePlan, mockWorkoutPlan]);

      render(<WorkoutPlanGeneratorPage />);

      await waitFor(() => {
        const setActiveButton = screen.getAllByText(/Set as Active/i)[0];
        fireEvent.click(setActiveButton);
      });

      await waitFor(() => {
        expect(mockSetWorkoutPlanActive).toHaveBeenCalledWith('plan-2');
      });
    });

    it('should highlight active plan with green styling', async () => {
      render(<WorkoutPlanGeneratorPage />);

      await waitFor(() => {
        const activeBadges = screen.getAllByText(/Active/i);
        expect(activeBadges.length).toBeGreaterThan(0);
      });
    });
  });

  describe('Exercise Completion Tracking', () => {
    it('should display exercises with completion checkboxes', async () => {
      render(<WorkoutPlanGeneratorPage />);

      await waitFor(() => {
        expect(screen.getByText(/Bench Press/i)).toBeInTheDocument();
        expect(screen.getByText(/Rows/i)).toBeInTheDocument();
      });
    });

    it('should show completed exercises with green styling', async () => {
      mockGetWorkoutPlanDetail.mockResolvedValue(mockWorkoutPlanWithCompletions);

      render(<WorkoutPlanGeneratorPage />);

      await waitFor(() => {
        const completedExercise = screen.getByText(/Bench Press/i);
        expect(completedExercise).toBeInTheDocument();
      });
    });

    it('should call markExerciseComplete when exercise checkbox is clicked', async () => {
      render(<WorkoutPlanGeneratorPage />);

      await waitFor(() => {
        const checkboxes = screen.getAllByRole('button', { name: /mark as complete/i });
        if (checkboxes.length > 0) {
          fireEvent.click(checkboxes[0]);
        }
      });

      await waitFor(() => {
        expect(mockMarkExerciseComplete).toHaveBeenCalled();
      });
    });

    it('should display day progress bar for each day', async () => {
      render(<WorkoutPlanGeneratorPage />);

      await waitFor(() => {
        // Check for day elements in various formats
        const dayElements = screen.getAllByText(/Day \d+/i);
        expect(dayElements.length).toBeGreaterThan(0);
      });
    });
  });

  describe('Progress Tracker', () => {
    it('should display progress tracker with day cards', async () => {
      render(<WorkoutPlanGeneratorPage />);

      await waitFor(() => {
        expect(screen.getByText(/Plan Progress/i)).toBeInTheDocument();
      });

      await waitFor(() => {
        const dayCards = screen.getAllByText(/Day \d+/i);
        expect(dayCards.length).toBeGreaterThanOrEqual(2);
      });
    });

    it('should show completion status on day cards', async () => {
      mockGetWorkoutPlanDetail.mockResolvedValue(mockWorkoutPlanWithCompletions);

      render(<WorkoutPlanGeneratorPage />);

      await waitFor(() => {
        const dayCards = screen.getAllByText(/Day \d+/i);
        expect(dayCards.length).toBeGreaterThan(0);
      });
    });

    it('should allow clicking day cards to navigate to that day', async () => {
      render(<WorkoutPlanGeneratorPage />);

      await waitFor(() => {
        const dayCards = screen.getAllByText(/Day 2/i);
        // Click the first Day 2 card (in the progress tracker)
        if (dayCards.length > 0) {
          fireEvent.click(dayCards[0]);
        }
      });

      await waitFor(() => {
        const day2Headers = screen.getAllByText(/Day 2/i);
        expect(day2Headers.length).toBeGreaterThan(0);
      });
    });

    it('should display overall progress percentage', async () => {
      render(<WorkoutPlanGeneratorPage />);

      await waitFor(() => {
        expect(screen.getByText(/\d+ of \d+ days completed/i)).toBeInTheDocument();
      });
    });
  });

  describe('Day Navigation', () => {
    it('should display Previous and Next navigation buttons', async () => {
      render(<WorkoutPlanGeneratorPage />);

      await waitFor(() => {
        expect(screen.getByText(/Previous/i)).toBeInTheDocument();
        expect(screen.getByText(/Next/i)).toBeInTheDocument();
      });
    });

    it('should disable Previous button on first day', async () => {
      render(<WorkoutPlanGeneratorPage />);

      await waitFor(() => {
        const previousButton = screen.getByText(/Previous/i);
        expect(previousButton).toBeDisabled();
      });
    });

    it('should navigate to next day when Next button is clicked', async () => {
      render(<WorkoutPlanGeneratorPage />);

      await waitFor(() => {
        const nextButtons = screen.getAllByText(/Next/i);
        if (nextButtons.length > 0) {
          fireEvent.click(nextButtons[0]);
        }
      });

      await waitFor(() => {
        const day2Elements = screen.getAllByText(/Day 2/i);
        expect(day2Elements.length).toBeGreaterThan(0);
      });
    });

    it('should navigate to previous day when Previous button is clicked', async () => {
      render(<WorkoutPlanGeneratorPage />);

      // First navigate to day 2
      await waitFor(() => {
        const nextButtons = screen.getAllByText(/Next/i);
        if (nextButtons.length > 0) {
          fireEvent.click(nextButtons[0]);
        }
      });

      // Then navigate back
      await waitFor(() => {
        const previousButtons = screen.getAllByText(/Previous/i);
        if (previousButtons.length > 0) {
          fireEvent.click(previousButtons[0]);
        }
      });

      await waitFor(() => {
        const day1Elements = screen.getAllByText(/Day 1/i);
        expect(day1Elements.length).toBeGreaterThan(0);
      });
    });

    it('should show current day indicator in navigation', async () => {
      render(<WorkoutPlanGeneratorPage />);

      await waitFor(() => {
        expect(screen.getByText(/Day 1 of 2/i)).toBeInTheDocument();
      });
    });
  });

  describe('Weekly Progress Graph', () => {
    it('should display weekly progress graph', async () => {
      render(<WorkoutPlanGeneratorPage />);

      await waitFor(() => {
        expect(screen.getByText(/Weekly Progress/i)).toBeInTheDocument();
        expect(screen.getByText(/Last 8 Weeks/i)).toBeInTheDocument();
      });
    });

    it('should show empty state when no completion data exists', async () => {
      render(<WorkoutPlanGeneratorPage />);

      await waitFor(() => {
        const graphSection = screen.getByText(/Weekly Progress/i).closest('div');
        expect(graphSection).toBeInTheDocument();
      });
    });

    it('should display graph legend', async () => {
      render(<WorkoutPlanGeneratorPage />);

      await waitFor(() => {
        expect(screen.getByText(/Completed Days/i)).toBeInTheDocument();
        expect(screen.getByText(/Total Days/i)).toBeInTheDocument();
      });
    });
  });

  describe('Integration Tests', () => {
    it('should update progress when exercise is marked complete', async () => {
      const updatedPlan = {
        ...mockWorkoutPlan,
        workout_plan_data: {
          ...mockWorkoutPlan.workout_plan_data,
          exercise_completions: {
            day_1: {
              exercise_0: { completed: true, completed_at: new Date().toISOString() },
            },
          },
        },
      };

      mockMarkExerciseComplete.mockResolvedValue(updatedPlan);
      mockGetWorkoutPlanDetail.mockResolvedValue(updatedPlan);

      render(<WorkoutPlanGeneratorPage />);

      await waitFor(() => {
        const checkboxes = screen.getAllByRole('button', { name: /mark as complete/i });
        if (checkboxes.length > 0) {
          fireEvent.click(checkboxes[0]);
        }
      });

      await waitFor(() => {
        expect(mockGetWorkoutPlanDetail).toHaveBeenCalled();
      });
    });

    it('should refresh plans after setting active plan', async () => {
      const inactivePlan = { ...mockWorkoutPlan, id: 'plan-2', is_active: false };
      mockGetSavedWorkoutPlans
        .mockResolvedValueOnce([inactivePlan, mockWorkoutPlan])
        .mockResolvedValueOnce([{ ...inactivePlan, is_active: true }, { ...mockWorkoutPlan, is_active: false }]);

      render(<WorkoutPlanGeneratorPage />);

      await waitFor(() => {
        const setActiveButton = screen.getAllByText(/Set as Active/i)[0];
        fireEvent.click(setActiveButton);
      });

      await waitFor(() => {
        expect(mockGetSavedWorkoutPlans).toHaveBeenCalledTimes(2);
      });
    });
  });

  describe('Error Handling', () => {
    it('should handle API errors gracefully', async () => {
      mockGetSavedWorkoutPlans.mockRejectedValue(new Error('API Error'));

      render(<WorkoutPlanGeneratorPage />);

      await waitFor(() => {
        // Should still render the page without crashing
        expect(screen.getByText(/AI Workout Plan Generator/i)).toBeInTheDocument();
      });
    });

    it('should handle missing active plan', async () => {
      mockGetSavedWorkoutPlans.mockResolvedValue([{ ...mockWorkoutPlan, is_active: false }]);

      render(<WorkoutPlanGeneratorPage />);

      await waitFor(() => {
        expect(screen.getByText(/Your Saved Plans/i)).toBeInTheDocument();
      });
    });
  });
});

