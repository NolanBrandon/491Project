import { render, screen, fireEvent, waitFor, within, act } from '@testing-library/react';
import '@testing-library/jest-dom';
import userEvent from '@testing-library/user-event';
import WorkoutPlanGeneratorPage from '../workout-plan-generator/page';
import * as goalsApi from '@/lib/goalsApi';
import * as aiWorkoutPlanApi from '@/lib/aiWorkoutPlanApi';
import * as workoutPlansApi from '@/lib/workoutPlansApi';

// Mock Next.js navigation
const mockPush = jest.fn();
const mockReplace = jest.fn();
const mockPrefetch = jest.fn();

jest.mock('next/navigation', () => ({
  useRouter: () => ({
    push: mockPush,
    replace: mockReplace,
    prefetch: mockPrefetch,
  }),
  usePathname: () => '/workout-plan-generator',
  useSearchParams: () => new URLSearchParams(),
}));

// Mock Link component
jest.mock('next/link', () => {
  return ({ children, href }: { children: React.ReactNode; href: string }) => {
    return <a href={href}>{children}</a>;
  };
});

// Mock AuthContext
const mockUser = {
  id: 'test-user-id',
  username: 'testuser',
  email: 'test@example.com',
};

const mockAuth = {
  user: mockUser,
  isAuthenticated: true,
  loading: false,
  refreshUser: jest.fn(),
  logout: jest.fn(),
};

jest.mock('@/contexts/AuthContext', () => ({
  useAuth: () => mockAuth,
}));

// Mock Navbar component
jest.mock('@/app/components/navbar', () => {
  return function Navbar() {
    return <nav data-testid="navbar">Navbar</nav>;
  };
});

// Mock RecentWorkoutsModal component
jest.mock('@/components/workouts/RecentWorkoutsModal', () => {
  return function RecentWorkoutsModal({
    isOpen,
    onClose,
    onAddExercises,
    existingExerciseNames,
  }: {
    isOpen: boolean;
    onClose: () => void;
    onAddExercises: (exercises: any[]) => void;
    existingExerciseNames: string[];
  }) {
    if (!isOpen) return null;
    
    const handleAddExercises = () => {
      onAddExercises([
        { exercise_name: 'Push-ups', sets_performed: 3, reps_performed: 10 },
        { exercise_name: 'Squats', sets_performed: 3, reps_performed: 12 },
      ]);
      // Modal closes automatically after adding exercises (via onClose callback)
      onClose();
    };
    
    return (
      <div data-testid="recent-workouts-modal">
        <div>Recent Workouts Modal</div>
        <div data-testid="existing-exercises">
          Existing: {existingExerciseNames.join(', ')}
        </div>
        <button onClick={handleAddExercises}>Add Exercises</button>
        <button onClick={onClose}>Close</button>
      </div>
    );
  };
});

// Mock API modules
jest.mock('@/lib/goalsApi');
jest.mock('@/lib/aiWorkoutPlanApi');
jest.mock('@/lib/workoutPlansApi');

const mockGetGoals = goalsApi.getGoals as jest.MockedFunction<typeof goalsApi.getGoals>;
const mockGetSavedWorkoutPlans = aiWorkoutPlanApi.getSavedWorkoutPlans as jest.MockedFunction<typeof aiWorkoutPlanApi.getSavedWorkoutPlans>;
const mockGenerateWorkoutPlan = aiWorkoutPlanApi.generateWorkoutPlan as jest.MockedFunction<typeof aiWorkoutPlanApi.generateWorkoutPlan>;

describe('WorkoutPlanGeneratorPage', () => {
  const mockGoal: goalsApi.Goal = {
    id: 'goal-1',
    title: 'Build Muscle',
    description: 'I want to build muscle',
    status: 'active',
    is_active: true,
    target_date: '2024-12-31',
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-01T00:00:00Z',
    user: mockUser.id,
    goal_type: 'muscle_gain',
    target_weight_kg: null,
    start_date: '2024-01-01',
    end_date: null,
  };

  const mockSavedPlans: aiWorkoutPlanApi.WorkoutPlan[] = [
    {
      id: 'plan-1',
      name: 'Upper Body Plan',
      description: 'A great upper body plan',
      created_at: '2024-01-01T00:00:00Z',
      user: mockUser.id,
      workout_plan_data: {
        success: true,
        data: {
          plan_name: 'Upper Body Plan',
          plan_description: 'A great upper body plan',
          days: [],
        },
        message: 'Generated successfully',
        enrichment_stats: {
          total_exercises: 0,
          detailed_enriched: 0,
          search_enriched: 0,
          ai_only: 0,
          total_enriched: 0,
          enrichment_rate: 0,
          high_confidence_matches: 0,
          medium_confidence_matches: 0,
          no_matches: 0,
          high_confidence_rate: 0,
          muscles_auto_populated: 0,
          equipments_auto_populated: 0,
          body_parts_auto_populated: 0,
          keywords_auto_populated: 0,
        },
      },
    },
  ];

  beforeEach(() => {
    jest.clearAllMocks();
    
    // Default mocks
    mockGetGoals.mockResolvedValue([mockGoal]);
    mockGetSavedWorkoutPlans.mockResolvedValue(mockSavedPlans);
    mockGenerateWorkoutPlan.mockResolvedValue({
      success: true,
      saved_plan_id: 'new-plan-id',
      data: {
        plan_name: 'Generated Plan',
        plan_description: 'A generated plan',
        days: [],
      },
      enrichment_stats: {
        total_exercises: 0,
        detailed_enriched: 0,
        search_enriched: 0,
        ai_only: 0,
        total_enriched: 0,
        enrichment_rate: 0,
        high_confidence_matches: 0,
        medium_confidence_matches: 0,
        no_matches: 0,
        high_confidence_rate: 0,
        muscles_auto_populated: 0,
        equipments_auto_populated: 0,
        body_parts_auto_populated: 0,
        keywords_auto_populated: 0,
      },
      message: 'Generated successfully',
      user_id: mockUser.id,
      generation_params: {
        user_goal: mockGoal.description || mockGoal.title,
        experience_level: 'beginner',
        days_per_week: 4,
      },
    });

    // Mock fetch for plan updates
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({
          id: 'new-plan-id',
          workout_plan_data: { days: [] },
        }),
      })
    ) as jest.Mock;
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  describe('Rendering', () => {
    it('renders workout plan generator heading', async () => {
      await act(async () => {
        render(<WorkoutPlanGeneratorPage />);
      });
      
      await waitFor(() => {
        expect(screen.getByRole('heading', { name: /ai workout plan generator/i })).toBeInTheDocument();
      });
    });

    it('renders navbar', () => {
      render(<WorkoutPlanGeneratorPage />);
      expect(screen.getByTestId('navbar')).toBeInTheDocument();
    });

    it('shows loading state for goals', async () => {
      mockGetGoals.mockImplementation(() => new Promise(() => {})); // Never resolves
      await act(async () => {
        render(<WorkoutPlanGeneratorPage />);
      });
      expect(screen.getByText(/loading your goals/i)).toBeInTheDocument();
    });

    it('shows message when no active goal', async () => {
      mockGetGoals.mockResolvedValue([]);
      await act(async () => {
        render(<WorkoutPlanGeneratorPage />);
      });
      
      await waitFor(() => {
        expect(screen.getByText(/no active goal found/i)).toBeInTheDocument();
      });
    });

    it('displays active goal when available', async () => {
      await act(async () => {
        render(<WorkoutPlanGeneratorPage />);
      });
      
      await waitFor(() => {
        expect(screen.getByText(mockGoal.title)).toBeInTheDocument();
      });
    });
  });

  describe('Workout Plan Form', () => {
    beforeEach(async () => {
      await act(async () => {
        render(<WorkoutPlanGeneratorPage />);
      });
      await waitFor(() => {
        expect(screen.getByText(mockGoal.title)).toBeInTheDocument();
      });
    });

    it('renders experience level selector', async () => {
      const selector = await screen.findByLabelText(/experience level/i);
      expect(selector).toBeInTheDocument();
      expect(selector).toHaveValue('beginner');
    });

    it('renders days per week selector', async () => {
      const selector = await screen.findByLabelText(/days per week/i);
      expect(selector).toBeInTheDocument();
      expect(selector).toHaveValue('4');
    });

    it('renders save plan checkbox', () => {
      const checkbox = screen.getByLabelText(/save this plan to my account/i);
      expect(checkbox).toBeInTheDocument();
      expect(checkbox).toBeChecked();
    });

    it('renders generate workout plan button', () => {
      const button = screen.getByRole('button', { name: /generate workout plan/i });
      expect(button).toBeInTheDocument();
    });

    it('allows changing experience level', async () => {
      const selector = screen.getByLabelText(/experience level/i);
      await userEvent.selectOptions(selector, 'intermediate');
      expect(selector).toHaveValue('intermediate');
    });

    it('allows changing days per week', async () => {
      const selector = screen.getByLabelText(/days per week/i);
      await userEvent.selectOptions(selector, '5');
      expect(selector).toHaveValue('5');
    });

    it('allows toggling save plan checkbox', async () => {
      const checkbox = screen.getByLabelText(/save this plan to my account/i);
      await userEvent.click(checkbox);
      expect(checkbox).not.toBeChecked();
    });
  });

  describe('Recent Workouts Feature', () => {
    beforeEach(async () => {
      await act(async () => {
        render(<WorkoutPlanGeneratorPage />);
      });
      await waitFor(() => {
        expect(screen.getByText(mockGoal.title)).toBeInTheDocument();
      });
    });

    it('renders add exercises from recent workouts button', () => {
      const button = screen.getByRole('button', { name: /add exercises from recent workouts/i });
      expect(button).toBeInTheDocument();
    });

    it('opens recent workouts modal when button is clicked', async () => {
      const button = screen.getByRole('button', { name: /add exercises from recent workouts/i });
      await userEvent.click(button);
      
      expect(screen.getByTestId('recent-workouts-modal')).toBeInTheDocument();
    });

    it('closes modal when close is clicked', async () => {
      const openButton = screen.getByRole('button', { name: /add exercises from recent workouts/i });
      await userEvent.click(openButton);
      
      const modal = screen.getByTestId('recent-workouts-modal');
      const closeButton = within(modal).getByRole('button', { name: /close/i });
      await userEvent.click(closeButton);
      
      await waitFor(() => {
        expect(screen.queryByTestId('recent-workouts-modal')).not.toBeInTheDocument();
      });
    });

    it('displays selected exercises after adding from recent workouts', async () => {
      const openButton = screen.getByRole('button', { name: /add exercises from recent workouts/i });
      await userEvent.click(openButton);
      
      const modal = screen.getByTestId('recent-workouts-modal');
      const addButton = within(modal).getByRole('button', { name: /add exercises/i });
      await userEvent.click(addButton);
      
      // Wait for modal to close and selected exercises section to appear
      await waitFor(() => {
        expect(screen.queryByTestId('recent-workouts-modal')).not.toBeInTheDocument();
        expect(screen.getByRole('heading', { name: /exercises from recent workouts/i })).toBeInTheDocument();
      }, { timeout: 3000 });
      
      // Check exercises in the selected exercises section (not in modal)
      await waitFor(() => {
        const heading = screen.getByRole('heading', { name: /exercises from recent workouts/i });
        const selectedSection = heading.closest('.bg-green-50');
        expect(selectedSection).toBeInTheDocument();
        const sectionText = selectedSection?.textContent || '';
        expect(sectionText).toMatch(/push-ups/i);
        expect(sectionText).toMatch(/squats/i);
      });
    });

    it('shows exercise count in selected exercises header', async () => {
      const openButton = screen.getByRole('button', { name: /add exercises from recent workouts/i });
      await userEvent.click(openButton);
      
      const modal = screen.getByTestId('recent-workouts-modal');
      const addButton = within(modal).getByRole('button', { name: /add exercises/i });
      await userEvent.click(addButton);
      
      await waitFor(() => {
        expect(screen.getByRole('heading', { name: /exercises from recent workouts \(2\)/i })).toBeInTheDocument();
      });
    });

    it('allows removing individual exercises', async () => {
      const openButton = screen.getByRole('button', { name: /add exercises from recent workouts/i });
      await userEvent.click(openButton);
      
      const modal = screen.getByTestId('recent-workouts-modal');
      const addButton = within(modal).getByRole('button', { name: /add exercises/i });
      await userEvent.click(addButton);
      
      // Wait for modal to close and selected exercises section to appear
      await waitFor(() => {
        expect(screen.queryByTestId('recent-workouts-modal')).not.toBeInTheDocument();
        expect(screen.getByRole('heading', { name: /exercises from recent workouts/i })).toBeInTheDocument();
      }, { timeout: 3000 });
      
      // Find the selected exercises section container and wait for exercises to appear
      let selectedSection: HTMLElement | null = null;
      await waitFor(() => {
        const heading = screen.getByRole('heading', { name: /exercises from recent workouts/i });
        selectedSection = heading.closest('.bg-green-50') as HTMLElement;
        expect(selectedSection).toBeInTheDocument();
        expect(selectedSection?.textContent).toMatch(/push-ups/i);
      });
      
      expect(selectedSection).toBeInTheDocument();
      const removeButtons = within(selectedSection!).getAllByRole('button', { name: /remove/i });
      expect(removeButtons.length).toBeGreaterThan(0);
      await userEvent.click(removeButtons[0]);
      
      await waitFor(() => {
        const sectionText = selectedSection?.textContent || '';
        expect(sectionText).not.toMatch(/push-ups/i);
        expect(sectionText).toMatch(/squats/i);
      });
    });

    it('allows clearing all selected exercises', async () => {
      const openButton = screen.getByRole('button', { name: /add exercises from recent workouts/i });
      await userEvent.click(openButton);
      
      const modal = screen.getByTestId('recent-workouts-modal');
      const addButton = within(modal).getByRole('button', { name: /add exercises/i });
      await userEvent.click(addButton);
      
      await waitFor(() => {
        expect(screen.getByRole('heading', { name: /exercises from recent workouts/i })).toBeInTheDocument();
      });
      
      const clearAllButton = screen.getByRole('button', { name: /clear all/i });
      await userEvent.click(clearAllButton);
      
      await waitFor(() => {
        expect(screen.queryByRole('heading', { name: /exercises from recent workouts/i })).not.toBeInTheDocument();
      });
    });

    it('passes existing exercise names to modal for duplicate detection', async () => {
      // Add exercises first
      const openButton = screen.getByRole('button', { name: /add exercises from recent workouts/i });
      await userEvent.click(openButton);
      
      const modal1 = screen.getByTestId('recent-workouts-modal');
      const addButton = within(modal1).getByRole('button', { name: /add exercises/i });
      await userEvent.click(addButton);
      
      // Wait for modal to close and exercises to be added
      await waitFor(() => {
        expect(screen.queryByTestId('recent-workouts-modal')).not.toBeInTheDocument();
        expect(screen.getByRole('heading', { name: /exercises from recent workouts/i })).toBeInTheDocument();
      });
      
      // Open modal again
      const openButton2 = await screen.findByRole('button', { name: /add exercises from recent workouts/i });
      await userEvent.click(openButton2);
      
      // Check that existing exercises are passed
      await waitFor(() => {
        const modal2 = screen.getByTestId('recent-workouts-modal');
        const existingExercises = within(modal2).getByTestId('existing-exercises');
        expect(existingExercises).toHaveTextContent('Push-ups');
        expect(existingExercises).toHaveTextContent('Squats');
      });
    });

    it('hides selected exercises section when no exercises are selected', () => {
      expect(screen.queryByRole('heading', { name: /exercises from recent workouts/i })).not.toBeInTheDocument();
    });
  });

  describe('Workout Plan Generation', () => {
    beforeEach(async () => {
      await act(async () => {
        render(<WorkoutPlanGeneratorPage />);
      });
      await waitFor(() => {
        expect(screen.getByText(mockGoal.title)).toBeInTheDocument();
      });
    });

    it('generates workout plan on form submit', async () => {
      const generateButton = screen.getByRole('button', { name: /generate workout plan/i });
      await userEvent.click(generateButton);
      
      await waitFor(() => {
        expect(mockGenerateWorkoutPlan).toHaveBeenCalledWith(
          mockUser.id,
          mockGoal.description || mockGoal.title,
          'beginner',
          4,
          true
        );
      });
    });

    it('navigates to plan detail page after successful generation', async () => {
      const generateButton = screen.getByRole('button', { name: /generate workout plan/i });
      await userEvent.click(generateButton);
      
      await waitFor(() => {
        expect(mockPush).toHaveBeenCalledWith('/workout-plans/new-plan-id');
      });
    });

    it('merges selected exercises into generated plan', async () => {
      // Add exercises first
      const openButton = screen.getByRole('button', { name: /add exercises from recent workouts/i });
      await userEvent.click(openButton);
      
      const modal = screen.getByTestId('recent-workouts-modal');
      const addButton = within(modal).getByRole('button', { name: /add exercises/i });
      await userEvent.click(addButton);
      
      // Wait for modal to close and exercises to be added
      await waitFor(() => {
        expect(screen.queryByTestId('recent-workouts-modal')).not.toBeInTheDocument();
        expect(screen.getByRole('heading', { name: /exercises from recent workouts/i })).toBeInTheDocument();
      });
      
      // Generate plan
      const generateButton = screen.getByRole('button', { name: /generate workout plan/i });
      await userEvent.click(generateButton);
      
      await waitFor(() => {
        expect(mockGenerateWorkoutPlan).toHaveBeenCalled();
        expect(global.fetch).toHaveBeenCalled();
      });
    });

    it('shows loading state during generation', async () => {
      mockGenerateWorkoutPlan.mockImplementation(() => new Promise(() => {})); // Never resolves
      
      const generateButton = screen.getByRole('button', { name: /generate workout plan/i });
      await userEvent.click(generateButton);
      
      await waitFor(() => {
        expect(screen.getByText(/generating your plan/i)).toBeInTheDocument();
        expect(generateButton).toBeDisabled();
      });
    });

    it('displays error message on generation failure', async () => {
      mockGenerateWorkoutPlan.mockRejectedValue(new Error('Generation failed'));
      
      const generateButton = screen.getByRole('button', { name: /generate workout plan/i });
      await userEvent.click(generateButton);
      
      await waitFor(() => {
        expect(screen.getByText(/generation failed/i)).toBeInTheDocument();
      });
    });
  });

  describe('Saved Plans Display', () => {
    it('displays saved workout plans', async () => {
      await act(async () => {
        render(<WorkoutPlanGeneratorPage />);
      });
      
      await waitFor(() => {
        expect(screen.getByText(/your saved plans/i)).toBeInTheDocument();
        expect(screen.getByText(mockSavedPlans[0].name)).toBeInTheDocument();
      });
    });

    it('shows loading state for saved plans', async () => {
      mockGetSavedWorkoutPlans.mockImplementation(() => new Promise(() => {})); // Never resolves
      await act(async () => {
        render(<WorkoutPlanGeneratorPage />);
      });
      expect(screen.getByText(/loading your saved plans/i)).toBeInTheDocument();
    });

    it('shows message when no saved plans', async () => {
      mockGetSavedWorkoutPlans.mockResolvedValue([]);
      await act(async () => {
        render(<WorkoutPlanGeneratorPage />);
      });
      
      await waitFor(() => {
        expect(screen.getByText(/no saved workout plans yet/i)).toBeInTheDocument();
      });
    });
  });

  describe('Authentication', () => {
    it('redirects to login when not authenticated', async () => {
      mockAuth.isAuthenticated = false;
      mockAuth.loading = false;
      
      await act(async () => {
        render(<WorkoutPlanGeneratorPage />);
      });
      
      await waitFor(() => {
        expect(mockReplace).toHaveBeenCalledWith('/login');
      });
    });

    it('does not redirect when authenticated', async () => {
      mockAuth.isAuthenticated = true;
      mockAuth.loading = false;
      
      await act(async () => {
        render(<WorkoutPlanGeneratorPage />);
      });
      
      await waitFor(() => {
        expect(screen.getByText(mockGoal.title)).toBeInTheDocument();
      });
      
      expect(mockReplace).not.toHaveBeenCalled();
    });
  });
});

