'use client';

import { useState, useEffect } from 'react';
import { useRouter, useParams } from 'next/navigation';
import Link from 'next/link';
import { useAuth } from '@/contexts/AuthContext';
import { getWorkoutPlanDetail, WorkoutPlan, WorkoutDay, Exercise } from '@/lib/aiWorkoutPlanApi';

export default function WorkoutPlanDetailPage() {
  const router = useRouter();
  const params = useParams();
  const { isAuthenticated } = useAuth();
  const planId = params.id as string;

  const [workoutPlan, setWorkoutPlan] = useState<WorkoutPlan | null>(null);
  const [currentDayIndex, setCurrentDayIndex] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Redirect if not authenticated
  useEffect(() => {
    if (!isAuthenticated) {
      router.replace('/login');
    }
  }, [isAuthenticated, router]);

  // Fetch workout plan on mount
  useEffect(() => {
    if (!isAuthenticated || !planId) return;

    const fetchPlan = async () => {
      try {
        setLoading(true);
        const plan = await getWorkoutPlanDetail(planId);
        setWorkoutPlan(plan);
      } catch (err) {
        console.error('Error fetching workout plan:', err);
        setError('Failed to load workout plan. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchPlan();
  }, [isAuthenticated, planId]);

  if (!isAuthenticated) {
    return null;
  }

  if (loading) {
    return (
      <div className="page-container blur-bg min-h-screen p-4 py-8">
        <div className="max-w-4xl mx-auto">
          <div className="bg-white rounded-lg shadow-md p-6">
            <p className="text-gray-600">Loading workout plan...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error || !workoutPlan) {
    return (
      <div className="page-container blur-bg min-h-screen p-4 py-8">
        <div className="max-w-4xl mx-auto">
          <div className="bg-red-50 border border-red-300 rounded-lg p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-2">Error</h2>
            <p className="text-gray-700 mb-4">{error || 'Workout plan not found.'}</p>
            <Link
              href="/workout-plan-generator"
              className="inline-block bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded"
            >
              Back to Generator
            </Link>
          </div>
        </div>
      </div>
    );
  }

  // Extract plan data from the nested structure
  const planData = workoutPlan.workout_plan_data.data;
  const days = planData.days || [];
  const currentDay = days[currentDayIndex];

  const handlePreviousDay = () => {
    if (currentDayIndex > 0) {
      setCurrentDayIndex(currentDayIndex - 1);
    }
  };

  const handleNextDay = () => {
    if (currentDayIndex < days.length - 1) {
      setCurrentDayIndex(currentDayIndex + 1);
    }
  };

  return (
    <div className="page-container blur-bg min-h-screen p-4 py-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-6">
          <Link
            href="/workout-plan-generator"
            className="text-blue-600 hover:text-blue-800 font-medium mb-2 inline-block"
          >
            ← Back to Generator
          </Link>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">{workoutPlan.name}</h1>
          {workoutPlan.description && (
            <p className="text-gray-600">{workoutPlan.description}</p>
          )}
        </div>

        {/* Day Navigation */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <div className="flex items-center justify-between mb-4">
            <button
              onClick={handlePreviousDay}
              disabled={currentDayIndex === 0}
              className={`px-4 py-2 rounded font-semibold ${
                currentDayIndex === 0
                  ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                  : 'bg-blue-600 text-white hover:bg-blue-700'
              }`}
            >
              ← Previous
            </button>

            <div className="text-center">
              <h2 className="text-2xl font-bold text-gray-900">
                Day {currentDay.day_number}: {currentDay.day_name}
              </h2>
              <p className="text-gray-600 text-sm">
                {currentDayIndex + 1} of {days.length}
              </p>
            </div>

            <button
              onClick={handleNextDay}
              disabled={currentDayIndex === days.length - 1}
              className={`px-4 py-2 rounded font-semibold ${
                currentDayIndex === days.length - 1
                  ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                  : 'bg-blue-600 text-white hover:bg-blue-700'
              }`}
            >
              Next →
            </button>
          </div>

          {/* Day Tabs (Optional alternative navigation) */}
          <div className="flex gap-2 overflow-x-auto pb-2">
            {days.map((day, index) => (
              <button
                key={day.day_number}
                onClick={() => setCurrentDayIndex(index)}
                className={`px-3 py-1 rounded text-sm font-medium whitespace-nowrap ${
                  index === currentDayIndex
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                Day {day.day_number}
              </button>
            ))}
          </div>
        </div>

        {/* Exercises for Current Day */}
        <div className="space-y-4">
          {currentDay.exercises.map((exercise, index) => (
            <ExerciseCard key={index} exercise={exercise} />
          ))}
        </div>
      </div>
    </div>
  );
}

// Exercise Card Component
function ExerciseCard({ exercise }: { exercise: Exercise }) {
  const [expanded, setExpanded] = useState(false);
  const hasDetails = exercise.exercise_details;

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      {/* Exercise Header */}
      <div className="p-4">
        <div className="flex justify-between items-start mb-2">
          <div className="flex-1">
            <h3 className="text-xl font-bold text-gray-900">{exercise.exercise_name}</h3>
            {exercise.matched_exercise_name && exercise.matched_exercise_name !== exercise.exercise_name && (
              <p className="text-sm text-gray-500 italic">
                Matched: {exercise.matched_exercise_name}
              </p>
            )}
          </div>
          <div className="text-right">
            <p className="text-lg font-semibold text-blue-600">
              {exercise.sets} sets × {exercise.reps} reps
            </p>
          </div>
        </div>

        {/* Quick Info */}
        {hasDetails && (
          <div className="flex flex-wrap gap-2 mb-3">
            {exercise.exercise_details.bodyParts && exercise.exercise_details.bodyParts.length > 0 && (
              <span className="px-2 py-1 bg-purple-100 text-purple-800 text-xs font-medium rounded">
                {exercise.exercise_details.bodyParts.join(', ')}
              </span>
            )}
            {exercise.exercise_details.equipments && exercise.exercise_details.equipments.length > 0 && (
              <span className="px-2 py-1 bg-green-100 text-green-800 text-xs font-medium rounded">
                {exercise.exercise_details.equipments.join(', ')}
              </span>
            )}
            {exercise.match_confidence && (
              <span className={`px-2 py-1 text-xs font-medium rounded ${
                exercise.match_confidence === 'high' ? 'bg-blue-100 text-blue-800' :
                exercise.match_confidence === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                'bg-gray-100 text-gray-800'
              }`}>
                {exercise.match_confidence} confidence
              </span>
            )}
          </div>
        )}

        {/* Media (Image/Video) */}
        {hasDetails && (exercise.exercise_details.imageUrl || exercise.exercise_details.videoUrl) && (
          <div className="mb-3">
            {exercise.exercise_details.imageUrl && (
              <img
                src={exercise.exercise_details.imageUrl}
                alt={exercise.exercise_name}
                className="w-full max-w-md rounded-lg"
              />
            )}
          </div>
        )}

        {/* Expand/Collapse Button */}
        {hasDetails && (
          <button
            onClick={() => setExpanded(!expanded)}
            className="text-blue-600 hover:text-blue-800 font-medium text-sm"
          >
            {expanded ? '− Show Less' : '+ Show More Details'}
          </button>
        )}
      </div>

      {/* Expanded Details */}
      {expanded && hasDetails && (
        <div className="border-t border-gray-200 p-4 bg-gray-50">
          {/* Overview */}
          {exercise.exercise_details.overview && (
            <div className="mb-4">
              <h4 className="font-semibold text-gray-900 mb-1">Overview</h4>
              <p className="text-gray-700 text-sm">{exercise.exercise_details.overview}</p>
            </div>
          )}

          {/* Instructions */}
          {exercise.exercise_details.instructions && exercise.exercise_details.instructions.length > 0 && (
            <div className="mb-4">
              <h4 className="font-semibold text-gray-900 mb-1">Instructions</h4>
              <ol className="list-decimal list-inside space-y-1 text-gray-700 text-sm">
                {exercise.exercise_details.instructions.map((instruction, idx) => (
                  <li key={idx}>{instruction}</li>
                ))}
              </ol>
            </div>
          )}

          {/* Exercise Tips */}
          {exercise.exercise_details.exerciseTips && exercise.exercise_details.exerciseTips.length > 0 && (
            <div className="mb-4">
              <h4 className="font-semibold text-gray-900 mb-1">Tips</h4>
              <ul className="list-disc list-inside space-y-1 text-gray-700 text-sm">
                {exercise.exercise_details.exerciseTips.map((tip, idx) => (
                  <li key={idx}>{tip}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Target & Secondary Muscles */}
          {((exercise.exercise_details.targetMuscles && exercise.exercise_details.targetMuscles.length > 0) ||
            (exercise.exercise_details.secondaryMuscles && exercise.exercise_details.secondaryMuscles.length > 0)) && (
            <div className="mb-4">
              <h4 className="font-semibold text-gray-900 mb-1">Muscles Worked</h4>
              {exercise.exercise_details.targetMuscles && exercise.exercise_details.targetMuscles.length > 0 && (
                <p className="text-gray-700 text-sm">
                  <strong>Primary:</strong> {exercise.exercise_details.targetMuscles.join(', ')}
                </p>
              )}
              {exercise.exercise_details.secondaryMuscles && exercise.exercise_details.secondaryMuscles.length > 0 && (
                <p className="text-gray-700 text-sm">
                  <strong>Secondary:</strong> {exercise.exercise_details.secondaryMuscles.join(', ')}
                </p>
              )}
            </div>
          )}

          {/* Variations */}
          {exercise.exercise_details.variations && exercise.exercise_details.variations.length > 0 && (
            <div className="mb-4">
              <h4 className="font-semibold text-gray-900 mb-1">Variations</h4>
              <ul className="list-disc list-inside space-y-1 text-gray-700 text-sm">
                {exercise.exercise_details.variations.map((variation, idx) => (
                  <li key={idx}>{variation}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Video Link */}
          {exercise.exercise_details.videoUrl && (
            <div className="mb-4">
              <h4 className="font-semibold text-gray-900 mb-1">Video Demo</h4>
              <a
                href={exercise.exercise_details.videoUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 hover:text-blue-800 text-sm"
              >
                Watch Video →
              </a>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
