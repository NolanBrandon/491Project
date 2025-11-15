'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useAuth } from '@/contexts/AuthContext';
import { getGoals, Goal } from '@/lib/goalsApi';
import { generateWorkoutPlan, getSavedWorkoutPlans, WorkoutPlan } from '@/lib/aiWorkoutPlanApi';
import { getRecentWorkouts, RecentWorkoutExercise } from '@/lib/workoutPlansApi';
import RecentWorkoutsModal from '@/components/workouts/RecentWorkoutsModal';
import Navbar from '@/app/components/navbar';

export default function WorkoutPlanGeneratorPage() {
  const router = useRouter();
  const { isAuthenticated, user, loading: authLoading } = useAuth();

  const [activeGoal, setActiveGoal] = useState<Goal | null>(null);
  const [savedPlans, setSavedPlans] = useState<WorkoutPlan[]>([]);
  const [experienceLevel, setExperienceLevel] = useState<'beginner' | 'intermediate' | 'advanced'>('beginner');
  const [daysPerWeek, setDaysPerWeek] = useState<number>(4);
  const [savePlan, setSavePlan] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [loadingGoals, setLoadingGoals] = useState(true);
  const [loadingPlans, setLoadingPlans] = useState(true);
  
  // Recent workouts state
  const [selectedExercises, setSelectedExercises] = useState<RecentWorkoutExercise[]>([]);
  const [showRecentWorkoutsModal, setShowRecentWorkoutsModal] = useState(false);

  // Redirect if not authenticated
  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.replace('/login');
    }
  }, [authLoading, isAuthenticated, router]);

  // Fetch active goal on mount
  useEffect(() => {
    if (!isAuthenticated) return;

    const fetchActiveGoal = async () => {
      try {
        setLoadingGoals(true);
        const goals = await getGoals();
        const active = goals.find(g => g.status === 'active' && g.is_active);
        setActiveGoal(active || null);
      } catch (err) {
        console.error('Error fetching goals:', err);
        setError('Failed to load goals. Please try again.');
      } finally {
        setLoadingGoals(false);
      }
    };

    fetchActiveGoal();
  }, [isAuthenticated]);

  // Fetch saved workout plans
  useEffect(() => {
    if (!isAuthenticated) return;

    const fetchSavedPlans = async () => {
      try {
        setLoadingPlans(true);
        const plans = await getSavedWorkoutPlans();
        setSavedPlans(plans);
      } catch (err) {
        console.error('Error fetching saved plans:', err);
        // Don't set error for saved plans - it's not critical
      } finally {
        setLoadingPlans(false);
      }
    };

    fetchSavedPlans();
  }, [isAuthenticated]);

  const handleAddExercisesFromRecent = (exercises: RecentWorkoutExercise[]) => {
    // Add exercises to selected exercises, avoiding duplicates
    setSelectedExercises(prev => {
      const existingNames = prev.map(ex => ex.exercise_name.toLowerCase());
      const newExercises = exercises.filter(
        ex => !existingNames.includes(ex.exercise_name.toLowerCase())
      );
      return [...prev, ...newExercises];
    });
  };

  const handleRemoveExercise = (exerciseName: string) => {
    setSelectedExercises(prev =>
      prev.filter(ex => ex.exercise_name !== exerciseName)
    );
  };

  const handleGeneratePlan = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!user || !activeGoal) return;

    setError(null);
    setLoading(true);

    try {
      // Generate AI workout plan
      const response = await generateWorkoutPlan(
        user.id,
        activeGoal.description || activeGoal.title,
        experienceLevel,
        daysPerWeek,
        savePlan
      );

      console.log('Workout plan generated:', response);

      // If we have selected exercises from recent workouts, merge them into the plan
      if (selectedExercises.length > 0 && savePlan && response.saved_plan_id) {
        try {
          // Get the saved plan to merge exercises
          const planResponse = await fetch(
            `${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api'}/workout-plans/${response.saved_plan_id}/`,
            {
              method: 'GET',
              credentials: 'include',
              headers: { 'Content-Type': 'application/json' },
            }
          );

          if (planResponse.ok) {
            const planData = await planResponse.json();
            const workoutPlanData = planData.workout_plan_data?.data || planData.workout_plan_data;
            
            // Convert selected exercises to plan format
            const exercisesToAdd = selectedExercises.map(ex => ({
              exercise_name: ex.exercise_name,
              sets: ex.sets_performed,
              reps: ex.reps_performed.toString(),
              rest_seconds: 60,
            }));

            // Add exercises to the first day (or create a day if none exist)
            if (workoutPlanData.days && workoutPlanData.days.length > 0) {
              workoutPlanData.days[0].exercises = [
                ...exercisesToAdd,
                ...workoutPlanData.days[0].exercises,
              ];
            } else {
              workoutPlanData.days = [
                {
                  day_number: 1,
                  day_name: 'Day 1',
                  exercises: exercisesToAdd,
                },
              ];
            }

            // Update the plan with merged exercises
            await fetch(
              `${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api'}/workout-plans/${response.saved_plan_id}/`,
              {
                method: 'PATCH',
                credentials: 'include',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                  workout_plan_data: workoutPlanData,
                }),
              }
            );
          }
        } catch (mergeError) {
          console.error('Error merging exercises:', mergeError);
          // Continue anyway - the plan was already created
        }
      }

      // If plan was saved, navigate to the detail page
      if (savePlan && response.saved_plan_id) {
        router.push(`/workout-plans/${response.saved_plan_id}`);
      } else {
        // If not saved, we could show the plan inline or store in state
        // For now, let's just show success message
        alert('Workout plan generated successfully!');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate workout plan');
      console.error('Generate plan error:', err);
    } finally {
      setLoading(false);
    }
  };

  const getExistingExerciseNames = (): string[] => {
    return selectedExercises.map(ex => ex.exercise_name);
  };

  // Show loading state while checking authentication
  if (authLoading) {
    return (
      <div className="page-container blur-bg min-h-screen p-4 py-8">
        <div className="max-w-4xl mx-auto">
          <div className="bg-white rounded-lg shadow-md p-6">
            <p className="text-gray-600">Loading...</p>
          </div>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  return (
    <>
      <Navbar />
      <div className="page-container blur-bg min-h-screen p-4 py-8">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-3xl font-bold mb-6 text-gray-900">AI Workout Plan Generator</h1>

        {/* Loading state for goals */}
        {loadingGoals ? (
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <p className="text-gray-600">Loading your goals...</p>
          </div>
        ) : !activeGoal ? (
          /* No active goal - show message */
          <div className="bg-yellow-50 border border-yellow-300 rounded-lg p-6 mb-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-2">No Active Goal Found</h2>
            <p className="text-gray-700 mb-4">
              To generate a personalized workout plan, you need to have an active goal set up.
              Your goal helps the AI understand what you want to achieve.
            </p>
            <Link
              href="/goals/new"
              className="inline-block bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded"
            >
              Create a Goal
            </Link>
          </div>
        ) : (
          /* Active goal exists - show generation form */
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <h2 className="text-2xl font-bold mb-4 text-gray-900">Generate Your Workout Plan</h2>

            {/* Display current goal */}
            <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <h3 className="text-lg font-semibold !text-gray-900 mb-2">Your Active Goal</h3>
              <p className="text-gray-800 font-medium">{activeGoal.title}</p>
              {activeGoal.description && (
                <p className="text-gray-600 mt-1">{activeGoal.description}</p>
              )}
            </div>

            {/* Selected Exercises from Recent Workouts */}
            {selectedExercises.length > 0 && (
              <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg">
                <div className="flex justify-between items-center mb-3">
                  <h3 className="text-lg font-semibold text-gray-900">
                    Exercises from Recent Workouts ({selectedExercises.length})
                  </h3>
                  <button
                    type="button"
                    onClick={() => setSelectedExercises([])}
                    className="text-sm text-gray-600 hover:text-gray-900 font-medium"
                  >
                    Clear All
                  </button>
                </div>
                <div className="space-y-2">
                  {selectedExercises.map((exercise, index) => (
                    <div
                      key={index}
                      className="flex items-center justify-between bg-white p-2 rounded border border-gray-200"
                    >
                      <div className="flex-1">
                        <span className="font-medium text-gray-900">{exercise.exercise_name}</span>
                        <span className="ml-3 text-sm text-gray-600">
                          {exercise.sets_performed} sets × {exercise.reps_performed} reps
                        </span>
                      </div>
                      <button
                        type="button"
                        onClick={() => handleRemoveExercise(exercise.exercise_name)}
                        className="text-red-600 hover:text-red-800 text-sm font-medium ml-3"
                      >
                        Remove
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}

            <form onSubmit={handleGeneratePlan} className="space-y-4">
              {/* Add from Recent Workouts Button */}
              <div>
                <button
                  type="button"
                  onClick={() => setShowRecentWorkoutsModal(true)}
                  className="w-full px-4 py-2 bg-blue-100 hover:bg-blue-200 text-blue-700 rounded-md font-medium border border-blue-300 transition-colors"
                >
                  + Add Exercises from Recent Workouts
                </button>
              </div>

              {/* Experience Level */}
              <div>
                <label htmlFor="experienceLevel" className="block text-sm font-medium text-gray-700 mb-1">
                  Experience Level *
                </label>
                <select
                  id="experienceLevel"
                  value={experienceLevel}
                  onChange={e => setExperienceLevel(e.target.value as 'beginner' | 'intermediate' | 'advanced')}
                  required
                  className="w-full border border-gray-300 p-3 rounded text-gray-900 text-base focus:outline-none focus:ring-2 focus:ring-blue-600"
                >
                  <option value="beginner">Beginner - New to working out</option>
                  <option value="intermediate">Intermediate - Regular exercise routine</option>
                  <option value="advanced">Advanced - Experienced athlete</option>
                </select>
              </div>

              {/* Days Per Week */}
              <div>
                <label htmlFor="daysPerWeek" className="block text-sm font-medium text-gray-700 mb-1">
                  Days Per Week *
                </label>
                <select
                  id="daysPerWeek"
                  value={daysPerWeek}
                  onChange={e => setDaysPerWeek(Number(e.target.value))}
                  required
                  className="w-full border border-gray-300 p-3 rounded text-gray-900 text-base focus:outline-none focus:ring-2 focus:ring-blue-600"
                >
                  <option value={3}>3 days per week</option>
                  <option value={4}>4 days per week</option>
                  <option value={5}>5 days per week</option>
                  <option value={6}>6 days per week</option>
                </select>
              </div>

              {/* Save Plan Checkbox */}
              <div className="flex items-center">
                <input
                  id="savePlan"
                  type="checkbox"
                  checked={savePlan}
                  onChange={e => setSavePlan(e.target.checked)}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <label htmlFor="savePlan" className="ml-2 block text-sm text-gray-700">
                  Save this plan to my account
                </label>
              </div>

              {error && <p className="text-red-600 font-medium">{error}</p>}

              <button
                type="submit"
                className={`w-full py-3 rounded text-white font-semibold text-base ${
                  loading ? 'bg-gray-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'
                }`}
                disabled={loading}
              >
                {loading ? 'Generating Your Plan...' : 'Generate Workout Plan'}
              </button>
            </form>
          </div>
        )}

        {/* Saved Workout Plans */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-bold mb-4 text-gray-900">Your Saved Plans</h2>

          {loadingPlans ? (
            <p className="text-gray-600">Loading your saved plans...</p>
          ) : savedPlans.length === 0 ? (
            <p className="text-gray-600">No saved workout plans yet. Generate your first plan above!</p>
          ) : (
            <div className="grid gap-4 md:grid-cols-2">
              {savedPlans.map(plan => (
                <Link
                  key={plan.id}
                  href={`/workout-plans/${plan.id}`}
                  className="block p-4 border border-gray-300 rounded-lg hover:border-blue-500 hover:shadow-md transition-all"
                >
                  <h3 className="text-lg font-semibold text-gray-900 mb-1">{plan.name}</h3>
                  {plan.description && (
                    <p className="text-gray-600 text-sm mb-2">{plan.description}</p>
                  )}
                  <p className="text-gray-500 text-xs">
                    Created: {new Date(plan.created_at).toLocaleDateString()}
                  </p>
                </Link>
              ))}
            </div>
          )}
        </div>
      </div>
      </div>

      {/* Recent Workouts Modal */}
      <RecentWorkoutsModal
        isOpen={showRecentWorkoutsModal}
        onClose={() => setShowRecentWorkoutsModal(false)}
        onAddExercises={handleAddExercisesFromRecent}
        existingExerciseNames={getExistingExerciseNames()}
      />
    </>
  );
}
