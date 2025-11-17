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

  // Check if a day is fully completed (all exercises done)
  const isDayCompleted = (plan: WorkoutPlan, day: any, dayNumber: number): boolean => {
    if (!day.exercises || day.exercises.length === 0) return false;
    return day.exercises.every((_: any, exIdx: number) => 
      isExerciseCompleted(plan, dayNumber, exIdx)
    );
  };

  // Get weekly progress data for the graph
  const getWeeklyProgressData = (plan: WorkoutPlan): Array<{ week: string; completedDays: number; totalDays: number }> => {
    if (!plan || !plan.workout_plan_data) return [];
    
    const completions = plan.workout_plan_data.exercise_completions || {};
    const planData = plan.workout_plan_data?.data || plan.workout_plan_data;
    const days = planData?.days || [];
    
    // Group completions by week
    const weeklyData: { [key: string]: { completedDays: Set<number>; totalDays: number } } = {};
    
    // Initialize weeks (last 8 weeks)
    const today = new Date();
    for (let i = 7; i >= 0; i--) {
      const weekDate = new Date(today);
      weekDate.setDate(weekDate.getDate() - (i * 7));
      const weekStart = new Date(weekDate);
      weekStart.setDate(weekStart.getDate() - weekStart.getDay()); // Start of week (Sunday)
      weekStart.setHours(0, 0, 0, 0);
      const weekKey = weekStart.toISOString().split('T')[0];
      weeklyData[weekKey] = { completedDays: new Set(), totalDays: days.length };
    }
    
    // Process each day to find when it was completed
    days.forEach((day: any, dayIdx: number) => {
      const dayNumber = day.day_number || dayIdx + 1;
      const dayKey = `day_${dayNumber}`;
      const dayCompletions = completions[dayKey] || {};
      
      // Check if all exercises in this day are completed
      const allExercisesCompleted = day.exercises?.every((_: any, exIdx: number) => {
        const exKey = `exercise_${exIdx}`;
        return dayCompletions[exKey]?.completed === true;
      });
      
      if (allExercisesCompleted) {
        // Find the latest completion date for this day
        let latestCompletionDate: Date | null = null;
        day.exercises?.forEach((_: any, exIdx: number) => {
          const exKey = `exercise_${exIdx}`;
          const exCompletion = dayCompletions[exKey];
          if (exCompletion?.completed_at) {
            const completionDate = new Date(exCompletion.completed_at);
            if (!latestCompletionDate || completionDate > latestCompletionDate) {
              latestCompletionDate = completionDate;
            }
          }
        });
        
        // If we have a completion date, assign it to the appropriate week
        if (latestCompletionDate) {
          const weekStart = new Date(latestCompletionDate);
          weekStart.setDate(weekStart.getDate() - weekStart.getDay());
          weekStart.setHours(0, 0, 0, 0);
          const weekKey = weekStart.toISOString().split('T')[0];
          
          if (weeklyData[weekKey]) {
            weeklyData[weekKey].completedDays.add(dayNumber);
          }
        }
      }
    });
    
    // Convert to array format
    return Object.entries(weeklyData)
      .sort(([a], [b]) => a.localeCompare(b))
      .map(([weekKey, data]) => {
        const weekStart = new Date(weekKey);
        const weekEnd = new Date(weekStart);
        weekEnd.setDate(weekEnd.getDate() + 6);
        return {
          week: `${weekStart.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })} - ${weekEnd.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}`,
          completedDays: data.completedDays.size,
          totalDays: data.totalDays
        };
      });
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
            ) : (() => {
              const planData = activePlanDetail.workout_plan_data?.data || activePlanDetail.workout_plan_data;
              const days = planData?.days || [];
              
              if (days.length === 0) {
                return <p className="text-gray-600">No workout days found in this plan.</p>;
              }

              // Calculate overall plan progress
              const completedDays = days.filter((day: any, idx: number) => {
                const dayNumber = day.day_number || idx + 1;
                return isDayCompleted(activePlanDetail, day, dayNumber);
              }).length;
              const totalDays = days.length;
              const planProgress = Math.round((completedDays / totalDays) * 100);

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
                    {/* Progress Tracker */}
                    <div className="bg-gradient-to-r from-blue-50 to-green-50 rounded-lg p-4 mb-6 border-2 border-blue-200">
                      <div className="flex items-center justify-between mb-3">
                        <h3 className="text-lg font-bold text-gray-900">Plan Progress</h3>
                        <span className="text-sm font-semibold text-gray-700">
                          {completedDays} of {totalDays} days completed ({planProgress}%)
                        </span>
                      </div>
                      
                      {/* Overall Progress Bar */}
                      <div className="w-full bg-gray-200 rounded-full h-3 mb-4 shadow-inner">
                        <div
                          className="bg-gradient-to-r from-blue-500 to-green-500 h-3 rounded-full transition-all duration-500 shadow-sm"
                          style={{ width: `${planProgress}%` }}
                        />
                      </div>

                      {/* Day Progress Indicators */}
                      <div className="flex items-center justify-between gap-2">
                        {days.map((day: any, idx: number) => {
                          const dayNumber = day.day_number || idx + 1;
                          const isCompleted = isDayCompleted(activePlanDetail, day, dayNumber);
                          const isCurrent = idx === safeDayIndex;

                          return (
                            <button
                              key={idx}
                              onClick={() => setCurrentDayIndex(idx)}
                              className={`flex-1 p-3 rounded-lg border-2 transition-all ${
                                isCompleted
                                  ? 'bg-green-100 border-green-500 hover:bg-green-200 shadow-md'
                                  : isCurrent
                                  ? 'bg-blue-100 border-blue-500 hover:bg-blue-200 shadow-md'
                                  : 'bg-gray-50 border-gray-300 hover:bg-gray-100'
                              }`}
                            >
                              <div className="flex flex-col items-center gap-1">
                                <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm ${
                                  isCompleted
                                    ? 'bg-green-500 text-white'
                                    : isCurrent
                                    ? 'bg-blue-500 text-white'
                                    : 'bg-gray-300 text-gray-600'
                                }`}>
                                  {isCompleted ? (
                                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                                    </svg>
                                  ) : (
                                    dayNumber
                                  )}
                                </div>
                                <span className={`text-xs font-semibold ${
                                  isCompleted
                                    ? 'text-green-700'
                                    : isCurrent
                                    ? 'text-blue-700'
                                    : 'text-gray-600'
                                }`}>
                                  Day {dayNumber}
                                </span>
                                {day.day_name && (
                                  <span className={`text-xs truncate w-full text-center ${
                                    isCompleted || isCurrent
                                      ? 'text-gray-700'
                                      : 'text-gray-500'
                                  }`}>
                                    {day.day_name.length > 8 ? day.day_name.substring(0, 8) + '...' : day.day_name}
                                  </span>
                                )}
                              </div>
                            </button>
                          );
                        })}
                      </div>
                    </div>

                    {/* Weekly Progress Graph */}
                    {(() => {
                      const weeklyData = getWeeklyProgressData(activePlanDetail);
                      const maxCompleted = Math.max(...weeklyData.map(d => d.completedDays), 0);
                      const maxValue = Math.max(maxCompleted, weeklyData[0]?.totalDays || 1, 1);
                      const graphHeight = 200;
                      const graphWidth = Math.max(600, weeklyData.length * 80);
                      const padding = 50;
                      const barWidth = weeklyData.length > 0 ? (graphWidth - (padding * 2)) / weeklyData.length - 10 : 60;
                      
                      // Generate Y-axis labels dynamically
                      const yAxisSteps = maxValue <= 5 ? maxValue + 1 : 6;
                      const yAxisLabels = Array.from({ length: yAxisSteps }, (_, i) => 
                        Math.round((i / (yAxisSteps - 1)) * maxValue)
                      );
                      
                      if (weeklyData.length === 0) {
                        return (
                          <div className="bg-white rounded-lg p-6 mb-6 border-2 border-gray-200">
                            <h3 className="text-lg font-bold text-gray-900 mb-4">Weekly Progress (Last 8 Weeks)</h3>
                            <p className="text-gray-500 text-center py-8">No completion data yet. Complete some exercises to see your progress!</p>
                          </div>
                        );
                      }

                      return (
                        <div className="bg-white rounded-lg p-6 mb-6 border-2 border-gray-200">
                          <h3 className="text-lg font-bold text-gray-900 mb-4">Weekly Progress (Last 8 Weeks)</h3>
                          <div className="overflow-x-auto">
                            <svg width={graphWidth} height={graphHeight + 80} className="w-full min-w-full">
                              {/* Y-axis labels */}
                              {yAxisLabels.map((val) => {
                                const y = graphHeight - (val / maxValue) * (graphHeight - padding) + padding;
                                return (
                                  <g key={val}>
                                    <line
                                      x1={padding}
                                      y1={y}
                                      x2={graphWidth - padding}
                                      y2={y}
                                      stroke="#e5e7eb"
                                      strokeWidth="1"
                                      strokeDasharray="4,4"
                                    />
                                    <text
                                      x={padding - 10}
                                      y={y + 4}
                                      textAnchor="end"
                                      className="text-xs fill-gray-600"
                                    >
                                      {val}
                                    </text>
                                  </g>
                                );
                              })}
                              
                              {/* Bars for completed days */}
                              {weeklyData.map((data, idx) => {
                                const x = padding + idx * (barWidth + 10) + 5;
                                const barHeight = (data.completedDays / maxValue) * (graphHeight - padding);
                                const y = graphHeight - barHeight;
                                
                                return (
                                  <g key={idx}>
                                    {/* Background bar (total days) */}
                                    <rect
                                      x={x}
                                      y={padding}
                                      width={barWidth}
                                      height={graphHeight - padding}
                                      fill="#e5e7eb"
                                      rx="4"
                                    />
                                    {/* Completed days bar */}
                                    <rect
                                      x={x}
                                      y={y}
                                      width={barWidth}
                                      height={barHeight}
                                      fill={data.completedDays > 0 ? "#10b981" : "#9ca3af"}
                                      rx="4"
                                      className="transition-all duration-300"
                                    />
                                    {/* Value label on bar */}
                                    {data.completedDays > 0 && (
                                      <text
                                        x={x + barWidth / 2}
                                        y={y - 5}
                                        textAnchor="middle"
                                        className="text-xs font-semibold fill-gray-800"
                                      >
                                        {data.completedDays}
                                      </text>
                                    )}
                                    {/* Week label */}
                                    <text
                                      x={x + barWidth / 2}
                                      y={graphHeight + 25}
                                      textAnchor="middle"
                                      className="text-xs fill-gray-600"
                                    >
                                      {data.week.split(' - ')[0]}
                                    </text>
                                  </g>
                                );
                              })}
                              
                              {/* X-axis line */}
                              <line
                                x1={padding}
                                y1={graphHeight}
                                x2={graphWidth - padding}
                                y2={graphHeight}
                                stroke="#374151"
                                strokeWidth="2"
                              />
                              
                              {/* Y-axis line */}
                              <line
                                x1={padding}
                                y1={padding}
                                x2={padding}
                                y2={graphHeight}
                                stroke="#374151"
                                strokeWidth="2"
                              />
                            </svg>
                          </div>
                          <div className="flex items-center justify-center gap-4 mt-4">
                            <div className="flex items-center gap-2">
                              <div className="w-4 h-4 bg-green-500 rounded"></div>
                              <span className="text-sm text-gray-600">Completed Days</span>
                            </div>
                            <div className="flex items-center gap-2">
                              <div className="w-4 h-4 bg-gray-200 rounded"></div>
                              <span className="text-sm text-gray-600">Total Days</span>
                            </div>
                          </div>
                        </div>
                      );
                    })()}

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
            })()}
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
