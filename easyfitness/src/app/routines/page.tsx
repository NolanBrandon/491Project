'use client';

import { useState } from 'react';
import { supabase } from '../../lib/supabaseClient';
import ClientWrapper from '../ClientWrapper';

export default function RoutinesPage() {
  const [datePerformed, setDatePerformed] = useState('');
  const [exerciseName, setExerciseName] = useState('');
  const [weight, setWeight] = useState('');
  const [sets, setSets] = useState('');
  const [reps, setReps] = useState('');
  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setMessage('');

    const { data: { user } } = await supabase.auth.getUser();
    if (!user) {
      setMessage('You must be logged in to log workouts.');
      setIsLoading(false);
      return;
    }

    const { error } = await supabase.from('workout_log').insert({
      date_performed: datePerformed,
      exercise_name: exerciseName,
      weight: weight ? parseFloat(weight) : null,
      sets_performed: parseInt(sets),
      reps_performed: parseInt(reps),
      user_id: user.id,
    });

    if (error) {
      setMessage('Error adding workout: ' + error.message);
    } else {
      setMessage('Workout logged successfully!');
      setDatePerformed('');
      setExerciseName('');
      setWeight('');
      setSets('');
      setReps('');
    }

    setIsLoading(false);
  };

  return (
    <ClientWrapper>
      <h1 className="h1 text-center mb-6">Log a Workout</h1>

      <form className="auth-card space-y-4" onSubmit={handleSubmit}>
        <label>
          Date & Time:
          <input
            type="datetime-local"
            value={datePerformed}
            onChange={(e) => setDatePerformed(e.target.value)}
            required
            className="auth-input w-full"
          />
        </label>

        <label>
          Exercise Name:
          <input
            type="text"
            value={exerciseName}
            onChange={(e) => setExerciseName(e.target.value)}
            required
            className="auth-input w-full"
          />
        </label>

        <label>
          Weight (kg):
          <input
            type="number"
            value={weight}
            onChange={(e) => setWeight(e.target.value)}
            className="auth-input w-full"
            step="any"
          />
        </label>

        <label>
          Sets:
          <input
            type="number"
            value={sets}
            onChange={(e) => setSets(e.target.value)}
            required
            className="auth-input w-full"
          />
        </label>

        <label>
          Reps:
          <input
            type="number"
            value={reps}
            onChange={(e) => setReps(e.target.value)}
            required
            className="auth-input w-full"
          />
        </label>

        <button type="submit" className="auth-btn w-full" disabled={isLoading}>
          {isLoading ? 'Logging…' : 'Log Workout'}
        </button>

        {message && <p className="auth-muted text-center">{message}</p>}
      </form>
    </ClientWrapper>
  );
}
