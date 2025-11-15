'use client';

import React, { useState, useEffect } from 'react';
import { getRecentWorkouts, RecentWorkout, RecentWorkoutExercise } from '../../lib/workoutPlansApi';

interface RecentWorkoutsModalProps {
  isOpen: boolean;
  onClose: () => void;
  onAddExercises: (exercises: RecentWorkoutExercise[]) => void;
  existingExerciseNames?: string[]; // For duplicate detection
}

export default function RecentWorkoutsModal({
  isOpen,
  onClose,
  onAddExercises,
  existingExerciseNames = [],
}: RecentWorkoutsModalProps) {
  const [recentWorkouts, setRecentWorkouts] = useState<RecentWorkout[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedWorkout, setSelectedWorkout] = useState<RecentWorkout | null>(null);
  const [selectedExercises, setSelectedExercises] = useState<Set<string>>(new Set());

  useEffect(() => {
    if (isOpen) {
      loadRecentWorkouts();
    } else {
      // Reset state when modal closes
      setRecentWorkouts([]);
      setSelectedWorkout(null);
      setSelectedExercises(new Set());
      setError(null);
    }
  }, [isOpen]);

  const loadRecentWorkouts = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await getRecentWorkouts(10, 30);
      setRecentWorkouts(response.recent_workouts || []);
    } catch (err) {
      console.error('Error loading recent workouts:', err);
      setError(err instanceof Error ? err.message : 'Failed to load recent workouts');
    } finally {
      setLoading(false);
    }
  };

  const handleWorkoutSelect = (workout: RecentWorkout) => {
    setSelectedWorkout(workout);
    // Pre-select exercises that aren't duplicates
    const nonDuplicateExercises = workout.exercises
      .filter(ex => !isDuplicate(ex.exercise_name))
      .map(ex => ex.exercise_name);
    setSelectedExercises(new Set(nonDuplicateExercises));
  };

  const handleExerciseToggle = (exerciseName: string) => {
    setSelectedExercises(prev => {
      const newSet = new Set(prev);
      if (newSet.has(exerciseName)) {
        newSet.delete(exerciseName);
      } else {
        newSet.add(exerciseName);
      }
      return newSet;
    });
  };

  const handleQuickAdd = () => {
    if (!selectedWorkout) return;

    // Get selected exercises from the selected workout
    const exercisesToAdd = selectedWorkout.exercises.filter(ex =>
      selectedExercises.has(ex.exercise_name)
    );

    if (exercisesToAdd.length > 0) {
      onAddExercises(exercisesToAdd);
      onClose();
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      weekday: 'short',
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  const isDuplicate = (exerciseName: string) => {
    return existingExerciseNames.some(
      existing => existing.toLowerCase() === exerciseName.toLowerCase()
    );
  };

  if (!isOpen) return null;

  return (
    <div
      className="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4"
      aria-modal="true"
      role="dialog"
      onClick={(e) => {
        if (e.target === e.currentTarget) {
          onClose();
        }
      }}
    >
      <div
        className="bg-white rounded-lg shadow-2xl max-w-3xl w-full max-h-[90vh] overflow-y-auto"
        style={{
          backgroundColor: '#ffffff',
          color: '#000000',
        }}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="sticky top-0 bg-white border-b border-gray-200 p-6 z-10">
          <div className="flex justify-between items-center">
            <h2 className="text-2xl font-bold" style={{ color: '#000000' }}>
              Recent Workouts
            </h2>
            <button
              onClick={onClose}
              className="w-8 h-8 flex items-center justify-center rounded-full bg-gray-200 hover:bg-gray-300 text-gray-700 font-bold text-lg"
              aria-label="Close modal"
            >
              ×
            </button>
          </div>
          <p className="text-sm text-gray-600 mt-2">
            Select a recent workout to quickly add exercises to your current workout
          </p>
        </div>

        {/* Content */}
        <div className="p-6">
          {loading && (
            <div className="text-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
              <p className="text-gray-600">Loading recent workouts...</p>
            </div>
          )}

          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
              <p className="text-red-700">{error}</p>
              <button
                onClick={loadRecentWorkouts}
                className="mt-2 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 text-sm"
              >
                Retry
              </button>
            </div>
          )}

          {!loading && !error && recentWorkouts.length === 0 && (
            <div className="text-center py-12">
              <p className="text-gray-600 mb-4">No recent workouts found.</p>
              <p className="text-sm text-gray-500">
                Complete some workouts to see them here for quick re-adding.
              </p>
            </div>
          )}

          {!loading && !error && recentWorkouts.length > 0 && (
            <div className="space-y-4">
              {/* Workout List */}
              {!selectedWorkout ? (
                <div className="space-y-3">
                  {recentWorkouts.map((workout) => (
                    <div
                      key={workout.date}
                      onClick={() => handleWorkoutSelect(workout)}
                      className="border border-gray-200 rounded-lg p-4 cursor-pointer hover:border-blue-500 hover:shadow-md transition-all bg-white"
                    >
                      <div className="flex justify-between items-start">
                        <div className="flex-1">
                          <h3 className="text-lg font-semibold text-gray-900 mb-1">
                            {formatDate(workout.date)}
                          </h3>
                          <p className="text-sm text-gray-600">
                            {workout.exercise_count} {workout.exercise_count === 1 ? 'exercise' : 'exercises'}
                          </p>
                        </div>
                        <div className="text-right">
                          <button
                            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 text-sm font-medium"
                            onClick={(e) => {
                              e.stopPropagation();
                              handleWorkoutSelect(workout);
                            }}
                          >
                            Select
                          </button>
                        </div>
                      </div>
                      <div className="mt-2 flex flex-wrap gap-2">
                        {workout.exercises.slice(0, 3).map((exercise) => (
                          <span
                            key={exercise.exercise_name}
                            className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded"
                          >
                            {exercise.exercise_name}
                          </span>
                        ))}
                        {workout.exercises.length > 3 && (
                          <span className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">
                            +{workout.exercises.length - 3} more
                          </span>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                /* Exercise Selection */
                <div className="space-y-4">
                  <div className="flex items-center justify-between border-b border-gray-200 pb-3">
                    <div>
                      <h3 className="text-xl font-bold text-gray-900">
                        {formatDate(selectedWorkout.date)}
                      </h3>
                      <p className="text-sm text-gray-600">
                        Select exercises to add to your workout
                      </p>
                    </div>
                    <button
                      onClick={() => setSelectedWorkout(null)}
                      className="px-4 py-2 text-gray-700 hover:text-gray-900 text-sm font-medium"
                    >
                      ← Back
                    </button>
                  </div>

                  <div className="space-y-2 max-h-96 overflow-y-auto">
                    {selectedWorkout.exercises.map((exercise) => {
                      const isDup = isDuplicate(exercise.exercise_name);
                      const isSelected = selectedExercises.has(exercise.exercise_name);

                      return (
                        <div
                          key={exercise.exercise_name}
                          className={`border rounded-lg p-4 ${
                            isDup
                              ? 'bg-yellow-50 border-yellow-300'
                              : isSelected
                              ? 'bg-blue-50 border-blue-500'
                              : 'bg-white border-gray-200 hover:border-gray-300'
                          }`}
                        >
                          <div className="flex items-start justify-between">
                            <div className="flex-1">
                              <div className="flex items-center gap-2">
                                <input
                                  type="checkbox"
                                  checked={isSelected}
                                  onChange={() => handleExerciseToggle(exercise.exercise_name)}
                                  disabled={isDup}
                                  className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                                />
                                <h4 className="font-semibold text-gray-900">
                                  {exercise.exercise_name}
                                </h4>
                                {isDup && (
                                  <span className="px-2 py-1 bg-yellow-200 text-yellow-800 text-xs rounded font-medium">
                                    Already Added
                                  </span>
                                )}
                              </div>
                              <div className="ml-6 mt-2 text-sm text-gray-600">
                                <span>
                                  {exercise.sets_performed} sets × {exercise.reps_performed} reps
                                </span>
                                {exercise.duration_minutes && (
                                  <span className="ml-3">
                                    {exercise.duration_minutes} min
                                  </span>
                                )}
                              </div>
                            </div>
                          </div>
                        </div>
                      );
                    })}
                  </div>

                  <div className="flex justify-end gap-3 pt-4 border-t border-gray-200">
                    <button
                      onClick={() => setSelectedWorkout(null)}
                      className="px-6 py-2 rounded bg-gray-200 text-gray-700 hover:bg-gray-300 font-semibold"
                    >
                      Back
                    </button>
                    <button
                      onClick={handleQuickAdd}
                      disabled={selectedExercises.size === 0}
                      className={`px-6 py-2 rounded font-semibold ${
                        selectedExercises.size === 0
                          ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                          : 'bg-blue-600 text-white hover:bg-blue-700'
                      }`}
                    >
                      Add {selectedExercises.size} {selectedExercises.size === 1 ? 'Exercise' : 'Exercises'}
                    </button>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

