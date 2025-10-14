'use client';

import { useEffect, useState } from 'react';
import { supabase } from '../../lib/supabaseClient';
import ClientWrapper from '../ClientWrapper';

interface NutritionLog {
  id: string;
  date_eaten: string;
  meal_type: string;
  food_name: string;
  quantity: number; // protein in grams
}

interface WorkoutLog {
  id: string;
  date_performed: string;
  exercise_name: string;
  weight: number;
  sets_performed: number;
  reps_performed: number;
}

type LogEntry = (NutritionLog & { type: 'meal' }) | (WorkoutLog & { type: 'workout' });

export default function MyLogPage() {
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState('');

  useEffect(() => {
    const fetchLogs = async () => {
      const { data: { user } } = await supabase.auth.getUser();
      if (!user) {
        setMessage('You must be logged in to view your log.');
        setLoading(false);
        return;
      }

      const { data: meals, error: mealError } = await supabase
        .from('nutrition_log')
        .select('*')
        .eq('user_id', user.id);

      const { data: workouts, error: workoutError } = await supabase
        .from('workout_log')
        .select('*')
        .eq('user_id', user.id);

      if (mealError || workoutError) {
        setMessage('Error loading logs: ' + (mealError?.message || workoutError?.message));
        setLoading(false);
        return;
      }

      // Merge and sort by date
      const combined: LogEntry[] = [
        ...(meals?.map((m: NutritionLog) => ({ ...m, type: 'meal' })) || []),
        ...(workouts?.map((w: WorkoutLog) => ({ ...w, type: 'workout' })) || []),
      ].sort((a, b) => {
        const dateA = new Date('date_eaten' in a ? a.date_eaten : a.date_performed).getTime();
        const dateB = new Date('date_eaten' in b ? b.date_eaten : b.date_performed).getTime();
        return dateB - dateA; // descending
      });

      setLogs(combined);
      setLoading(false);
    };

    fetchLogs();
  }, []);

  return (
    <ClientWrapper>
      <h1 className="h1 text-center mb-6">My Log</h1>

      {loading ? (
        <p className="auth-muted text-center">Loading logs...</p>
      ) : message ? (
        <p className="auth-muted text-center">{message}</p>
      ) : logs.length === 0 ? (
        <p className="auth-muted text-center">No logs yet.</p>
      ) : (
        <div className="space-y-4">
          {logs.map((log) =>
            log.type === 'meal' ? (
              <div key={log.id} className="auth-card p-4 border rounded-xl shadow-md bg-white">
                <p><strong>Food:</strong> {log.food_name}</p>
                <p><strong>Meal Type:</strong> {log.meal_type}</p>
                <p><strong>Protein (g):</strong> {log.quantity}</p>
                <p><strong>Date:</strong> {new Date(log.date_eaten).toLocaleString()}</p>
              </div>
            ) : (
              <div key={log.id} className="auth-card p-4 border rounded-xl shadow-md bg-white">
                <p><strong>Exercise:</strong> {log.exercise_name}</p>
                <p><strong>Weight (kg):</strong> {log.weight ?? '-'}</p>
                <p><strong>Sets:</strong> {log.sets_performed}</p>
                <p><strong>Reps:</strong> {log.reps_performed}</p>
                <p><strong>Date:</strong> {new Date(log.date_performed).toLocaleString()}</p>
              </div>
            )
          )}
        </div>
      )}
    </ClientWrapper>
  );
}
