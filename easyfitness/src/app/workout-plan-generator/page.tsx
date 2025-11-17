'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useAuth } from '@/contexts/AuthContext';
import { getGoals, Goal } from '@/lib/goalsApi';
import { generateWorkoutPlan, getSavedWorkoutPlans, WorkoutPlan, getWorkoutPlanCompletionLogs, CompletionLog, setWorkoutPlanActive, markExerciseComplete, getWorkoutPlanDetail } from '@/lib/aiWorkoutPlanApi';
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
  const [completionLogs, setCompletionLogs] = useState<CompletionLog[]>([]);
  const [loadingProgress, setLoadingProgress] = useState(true);
  const [activePlanDetail, setActivePlanDetail] = useState<WorkoutPlan | null>(null);
  const [loadingActivePlan, setLoadingActivePlan] = useState(false);
  const [currentDayIndex, setCurrentDayIndex] = useState(0);

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

  // Fetch completion logs for progress tracking
  useEffect(() => {
    if (!isAuthenticated || savedPlans.length === 0) {
      if (savedPlans.length === 0 && !loadingPlans) {
        setLoadingProgress(false);
      }
      return;
    }

    const fetchAllCompletionLogs = async () => {
      try {
        setLoadingProgress(true);
        const allLogs: CompletionLog[] = [];
        
        // Fetch completion logs for each plan
        for (const plan of savedPlans) {
          try {
            const logs = await getWorkoutPlanCompletionLogs(plan.id);
            allLogs.push(...logs);
          } catch (err) {
            console.error(`Error fetching logs for plan ${plan.id}:`, err);
            // Continue with other plans even if one fails
          }
        }
        
        // Sort by date (most recent first)
        allLogs.sort((a, b) => new Date(b.logged_at).getTime() - new Date(a.logged_at).getTime());
        setCompletionLogs(allLogs);
      } catch (err) {
        console.error('Error fetching completion logs:', err);
      } finally {
        setLoadingProgress(false);
      }
    };

    fetchAllCompletionLogs();
  }, [isAuthenticated, savedPlans, loadingPlans]);

  // Fetch active plan detail when active plan changes
  useEffect(() => {
    if (!isAuthenticated) return;
    
    const activePlan = savedPlans.find(plan => plan.is_active);
    if (activePlan) {
      const fetchActivePlanDetail = async () => {
        try {
          setLoadingActivePlan(true);
          const detail = await getWorkoutPlanDetail(activePlan.id);
          setActivePlanDetail(detail);
          // Reset to first day when plan changes
          setCurrentDayIndex(0);
        } catch (err) {
          console.error('Error fetching active plan detail:', err);
        } finally {
          setLoadingActivePlan(false);
        }
      };
      fetchActivePlanDetail();
    } else {
      setActivePlanDetail(null);
      setCurrentDayIndex(0);
    }
  }, [isAuthenticated, savedPlans]);

  const handleGeneratePlan = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!user || !activeGoal) return;

    setError(null);
    setLoading(true);

    try {
      const response = await generateWorkoutPlan(
        user.id,
        activeGoal.description || activeGoal.title,
        experienceLevel,
        daysPerWeek,
        savePlan
      );

      console.log('Workout plan generated:', response);

      // If plan was saved, refresh plans and navigate to the detail page
      if (savePlan && response.saved_plan_id) {
        // Refresh saved plans to include the new one
        const plans = await getSavedWorkoutPlans();
        setSavedPlans(plans);
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

  // Calculate progress statistics
  const totalPlans = savedPlans.length;
  const completedPlans = savedPlans.filter(plan => plan.is_completed).length;
  const completionRate = totalPlans > 0 ? Math.round((completedPlans / totalPlans) * 100) : 0;
  const recentCompletions = completionLogs.filter(log => log.action === 'completed').slice(0, 5);
  const currentStreak = calculateStreak(completionLogs);
  const activePlan = savedPlans.find(plan => plan.is_active);

  // Handle setting a plan as active
  const handleSetActive = async (planId: string) => {
    try {
      await setWorkoutPlanActive(planId);
      // Refresh plans to get updated active status
      const plans = await getSavedWorkoutPlans();
      setSavedPlans(plans);
    } catch (err) {
      console.error('Error setting plan as active:', err);
      setError(err instanceof Error ? err.message : 'Failed to set plan as active');
    }
  };

  // Handle marking exercise as complete
  const handleExerciseToggle = async (planId: string, dayNumber: number, exerciseIndex: number, currentlyCompleted: boolean) => {
    try {
      await markExerciseComplete(planId, dayNumber, exerciseIndex, !currentlyCompleted);
      // Refresh active plan detail
      if (activePlanDetail && activePlanDetail.id === planId) {
        const updated = await getWorkoutPlanDetail(planId);
        setActivePlanDetail(updated);
      }
      // Refresh plans
      const plans = await getSavedWorkoutPlans();
      setSavedPlans(plans);
    } catch (err) {
      console.error('Error toggling exercise completion:', err);
      setError(err instanceof Error ? err.message : 'Failed to update exercise');
    }
  };

  // Check if an exercise is completed
  const isExerciseCompleted = (plan: WorkoutPlan, dayNumber: number, exerciseIndex: number): boolean => {
    const completions = plan.workout_plan_data?.exercise_completions;
    if (!completions) return false;
    const dayKey = `day_${dayNumber}`;
    const exerciseKey = `exercise_${exerciseIndex}`;
    return completions[dayKey]?.[exerciseKey]?.completed === true;
  };

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

            <form onSubmit={handleGeneratePlan} className="space-y-4">
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

        {/* Active Plan Exercise Tracking */}
        {activePlan && activePlanDetail && (
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h2 className="text-2xl font-bold text-gray-900">Active Plan: {activePlan.name}</h2>
                {activePlan.description && (
                  <p className="text-gray-600 text-sm mt-1">{activePlan.description}</p>
                )}
              </div>
              <span className="px-3 py-1 bg-green-100 text-green-800 text-sm font-semibold rounded-full">
                ✓ Active
              </span>
            </div>

            {loadingActivePlan ? (
              <p className="text-gray-600">Loading plan details...</p>
            ) : (
              (() => {
                const planData = activePlanDetail.workout_plan_data?.data || activePlanDetail.workout_plan_data;
                const days = planData?.days || [];
                
                if (days.length === 0) {
                  return <p className="text-gray-600">No workout days found in this plan.</p>;
                }

                // Ensure currentDayIndex is within bounds
                const safeDayIndex = Math.min(currentDayIndex, days.length - 1);
                const currentDay = days[safeDayIndex];
                const dayNumber = currentDay.day_number || safeDayIndex + 1;
                const completedExercises = currentDay.exercises?.filter((_: any, exIdx: number) => 
                  isExerciseCompleted(activePlanDetail, dayNumber, exIdx)
                ).length || 0;
                const totalExercises = currentDay.exercises?.length || 0;
                const dayProgress = totalExercises > 0 ? Math.round((completedExercises / totalExercises) * 100) : 0;

                const handlePreviousDay = () => {
                  if (safeDayIndex > 0) {
                    setCurrentDayIndex(safeDayIndex - 1);
                  }
                };

                const handleNextDay = () => {
                  if (safeDayIndex < days.length - 1) {
                    setCurrentDayIndex(safeDayIndex + 1);
                  }
                };

                return (
                  <div>
                    {/* Navigation Header */}
                    <div className="flex items-center justify-between mb-4">
                      <button
                        onClick={handlePreviousDay}
                        disabled={safeDayIndex === 0}
                        className={`px-4 py-2 rounded-lg font-semibold transition-all flex items-center gap-2 ${
                          safeDayIndex === 0
                            ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                            : 'bg-blue-600 text-white hover:bg-blue-700 shadow-md'
                        }`}
                      >
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                        </svg>
                        Previous
                      </button>

                      <div className="text-center">
                        <div className="flex items-center gap-2 mb-1">
                          {days.map((_: any, idx: number) => (
                            <div
                              key={idx}
                              className={`w-2 h-2 rounded-full transition-all ${
                                idx === safeDayIndex
                                  ? 'bg-blue-600 w-8'
                                  : idx < safeDayIndex
                                  ? 'bg-green-500'
                                  : 'bg-gray-300'
                              }`}
                            />
                          ))}
                        </div>
                        <p className="text-sm text-gray-600 font-medium">
                          Day {safeDayIndex + 1} of {days.length}
                        </p>
                      </div>

                      <button
                        onClick={handleNextDay}
                        disabled={safeDayIndex === days.length - 1}
                        className={`px-4 py-2 rounded-lg font-semibold transition-all flex items-center gap-2 ${
                          safeDayIndex === days.length - 1
                            ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                            : 'bg-blue-600 text-white hover:bg-blue-700 shadow-md'
                        }`}
                      >
                        Next
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                        </svg>
                      </button>
                    </div>

                    {/* Current Day Card */}
                    <div className="border-2 border-blue-300 rounded-lg p-6 bg-blue-50/30">
                      {/* Day Header */}
                      <div className="flex items-center justify-between mb-4 pb-4 border-b-2 border-blue-200">
                        <div className="flex items-center gap-3">
                          <div className="px-4 py-2 bg-blue-600 text-white font-bold text-lg rounded-lg shadow-md">
                            Day {dayNumber}
                          </div>
                          <div>
                            <h3 className="text-xl font-bold text-gray-900">
                              {currentDay.day_name || `Workout Day ${dayNumber}`}
                            </h3>
                            <p className="text-sm text-gray-600 mt-0.5">
                              {completedExercises} of {totalExercises} exercises completed
                            </p>
                          </div>
                        </div>
                      </div>
                      
                      {/* Day Progress Bar */}
                      <div className="w-full bg-gray-200 rounded-full h-3 mb-4 shadow-inner">
                        <div
                          className="bg-gradient-to-r from-blue-500 to-green-500 h-3 rounded-full transition-all duration-300 shadow-sm"
                          style={{ width: `${dayProgress}%` }}
                        />
                      </div>
                      <div className="text-xs text-gray-500 mb-4 text-center font-medium">
                        {dayProgress}% Complete
                      </div>

                      {/* Exercises */}
                      <div className="space-y-2">
                        {currentDay.exercises?.map((exercise: any, exIdx: number) => {
                          const isCompleted = isExerciseCompleted(activePlanDetail, dayNumber, exIdx);
                          return (
                            <div
                              key={exIdx}
                              className={`flex items-center justify-between p-3 rounded-lg border-2 ${
                                isCompleted
                                  ? 'bg-green-50 border-green-400 shadow-sm'
                                  : 'bg-white border-gray-300 shadow-sm'
                              }`}
                            >
                              <div className="flex items-center gap-3 flex-1">
                                {/* Day Badge on Exercise */}
                                <div className="px-2 py-1 bg-blue-100 text-blue-700 text-xs font-bold rounded border border-blue-300">
                                  D{dayNumber}
                                </div>
                                <button
                                  onClick={() => handleExerciseToggle(activePlanDetail.id, dayNumber, exIdx, isCompleted)}
                                  className={`w-7 h-7 rounded border-2 flex items-center justify-center transition-all shadow-sm ${
                                    isCompleted
                                      ? 'bg-green-500 border-green-600 text-white'
                                      : 'bg-white border-gray-400 hover:border-green-500 hover:bg-green-50'
                                  }`}
                                  title={`Day ${dayNumber} - ${isCompleted ? 'Mark as incomplete' : 'Mark as complete'}`}
                                >
                                  {isCompleted && (
                                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                                    </svg>
                                  )}
                                </button>
                                <div className="flex-1">
                                  <p className={`font-semibold text-base ${isCompleted ? 'text-green-800 line-through' : 'text-gray-900'}`}>
                                    {exercise.matched_exercise_name || exercise.exercise_name}
                                  </p>
                                  <p className="text-sm text-gray-600 mt-0.5">
                                    {exercise.sets} sets × {exercise.reps} reps
                                  </p>
                                </div>
                              </div>
                            </div>
                          );
                        })}
                      </div>
                    </div>
                  </div>
                );
              })()
            )}
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
                <div
                  key={plan.id}
                  className={`p-4 border rounded-lg transition-all ${
                    plan.is_active
                      ? 'border-green-500 bg-green-50'
                      : 'border-gray-300 hover:border-blue-500 hover:shadow-md'
                  }`}
                >
                  <div className="flex items-start justify-between mb-2">
                    <Link
                      href={`/workout-plans/${plan.id}`}
                      className="flex-1"
                    >
                      <h3 className="text-lg font-semibold text-gray-900 mb-1">{plan.name}</h3>
                      {plan.description && (
                        <p className="text-gray-600 text-sm mb-2">{plan.description}</p>
                      )}
                      <p className="text-gray-500 text-xs">
                        Created: {new Date(plan.created_at).toLocaleDateString()}
                      </p>
                    </Link>
                    {plan.is_active && (
                      <span className="px-2 py-1 bg-green-100 text-green-800 text-xs font-semibold rounded-full ml-2">
                        Active
                      </span>
                    )}
                  </div>
                  <div className="flex gap-2 mt-3">
                    {!plan.is_active && (
                      <button
                        onClick={() => handleSetActive(plan.id)}
                        className="px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded transition-colors"
                      >
                        Set as Active
                      </button>
                    )}
                    <Link
                      href={`/workout-plans/${plan.id}`}
                      className="px-3 py-1.5 bg-gray-200 hover:bg-gray-300 text-gray-700 text-sm font-medium rounded transition-colors"
                    >
                      View Details
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
    </>
  );
}

// Helper function to calculate current streak
function calculateStreak(logs: CompletionLog[]): number {
  if (logs.length === 0) return 0;
  
  // Sort logs by date (most recent first)
  const sortedLogs = [...logs].sort((a, b) => new Date(b.logged_at).getTime() - new Date(a.logged_at).getTime());
  
  // Only count completed actions
  const completedLogs = sortedLogs.filter(log => log.action === 'completed');
  if (completedLogs.length === 0) return 0;
  
  // Group by date
  const dates = new Set<string>();
  completedLogs.forEach(log => {
    const date = new Date(log.logged_at).toDateString();
    dates.add(date);
  });
  
  // Calculate consecutive days
  const sortedDates = Array.from(dates)
    .map(d => new Date(d))
    .sort((a, b) => b.getTime() - a.getTime());
  
  if (sortedDates.length === 0) return 0;
  
  let streak = 1;
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  
  // Check if most recent completion was today or yesterday
  const mostRecent = new Date(sortedDates[0]);
  mostRecent.setHours(0, 0, 0, 0);
  const daysDiff = Math.floor((today.getTime() - mostRecent.getTime()) / (1000 * 60 * 60 * 24));
  
  if (daysDiff > 1) return 0; // Streak broken if more than 1 day ago
  
  // Count consecutive days
  for (let i = 1; i < sortedDates.length; i++) {
    const prev = new Date(sortedDates[i - 1]);
    const curr = new Date(sortedDates[i]);
    prev.setHours(0, 0, 0, 0);
    curr.setHours(0, 0, 0, 0);
    
    const diff = Math.floor((prev.getTime() - curr.getTime()) / (1000 * 60 * 60 * 24));
    if (diff === 1) {
      streak++;
    } else {
      break;
    }
  }
  
  return streak;
}
