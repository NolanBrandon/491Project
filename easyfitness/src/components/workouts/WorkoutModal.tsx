'use client';

import React, { useState } from 'react';
import {
  createWorkout,
  CreateWorkoutData,
} from '../../lib/workoutPlansApi';

interface WorkoutModalProps {
  isOpen: boolean;
  onClose: () => void;
  onWorkoutCreated: () => void;
}

export default function WorkoutModal({
  isOpen,
  onClose,
  onWorkoutCreated,
}: WorkoutModalProps) {
  const [formData, setFormData] = useState<CreateWorkoutData>({
    date_performed: new Date().toISOString().split('T')[0],
    sets_performed: 1,
    reps_performed: 1,
    duration_minutes: 0,
    calories_burned: 0,
    perceived_effort: 5,
    exercise_name: '',
    weight: 0,
    exercise_data: {},
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  if (!isOpen) return null;

  const handleChange = (field: keyof CreateWorkoutData, value: any) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      await createWorkout(formData);
      onWorkoutCreated();
      onClose();
    } catch (err) {
      console.error(err);
      setError('Failed to create workout.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className="workout-modal fixed inset-0 bg-black/60 flex items-center justify-center z-50"
      aria-modal="true"
      role="dialog"
    >
      <div
        className="rounded-lg shadow-2xl max-w-md w-full p-6 relative"
        style={{
          backgroundColor: '#ffffff',
          color: '#000000',
          border: '1px solid rgba(0,0,0,0.12)',
        }}
      >
        <h2
          className="text-2xl font-bold mb-4"
          style={{ color: '#000000' }}
        >
          Add Workout
        </h2>

        {error && <div className="text-red-700 mb-2">{error}</div>}

        <form onSubmit={handleSubmit} className="space-y-3 text-black">
          <label className="block">
            <div className="font-semibold text-sm mb-1" style={{ color: '#000' }}>Date Performed</div>
            <input
              type="date"
              value={formData.date_performed}
              onChange={(e) => handleChange('date_performed', e.target.value)}
              required
              style={{
                width: '100%',
                padding: '0.5rem',
                borderRadius: '0.375rem',
                border: '1px solid #cbd5e1',
                background: '#ffffff',
                color: '#000000',
              }}
            />
          </label>

          <label className="block">
            <div className="font-semibold text-sm mb-1" style={{ color: '#000' }}>Exercise Name</div>
            <input
              type="text"
              value={formData.exercise_name || ''}
              onChange={(e) => handleChange('exercise_name', e.target.value)}
              style={{
                width: '100%',
                padding: '0.5rem',
                borderRadius: '0.375rem',
                border: '1px solid #cbd5e1',
                background: '#ffffff',
                color: '#000000',
              }}
            />
          </label>

          <label className="block">
            <div className="font-semibold text-sm mb-1" style={{ color: '#000' }}>Sets Performed</div>
            <input
              type="number"
              value={formData.sets_performed}
              onChange={(e) => handleChange('sets_performed', Number(e.target.value))}
              min={1}
              required
              style={{
                width: '100%',
                padding: '0.5rem',
                borderRadius: '0.375rem',
                border: '1px solid #cbd5e1',
                background: '#ffffff',
                color: '#000000',
              }}
            />
          </label>

          <label className="block">
            <div className="font-semibold text-sm mb-1" style={{ color: '#000' }}>Reps Performed</div>
            <input
              type="number"
              value={formData.reps_performed}
              onChange={(e) => handleChange('reps_performed', Number(e.target.value))}
              min={1}
              required
              style={{
                width: '100%',
                padding: '0.5rem',
                borderRadius: '0.375rem',
                border: '1px solid #cbd5e1',
                background: '#ffffff',
                color: '#000000',
              }}
            />
          </label>

          <label className="block">
            <div className="font-semibold text-sm mb-1" style={{ color: '#000' }}>Duration (minutes)</div>
            <input
              type="number"
              value={formData.duration_minutes ?? ''}
              onChange={(e) => handleChange('duration_minutes', Number(e.target.value))}
              min={0}
              style={{
                width: '100%',
                padding: '0.5rem',
                borderRadius: '0.375rem',
                border: '1px solid #cbd5e1',
                background: '#ffffff',
                color: '#000000',
              }}
            />
          </label>

          <label className="block">
            <div className="font-semibold text-sm mb-1" style={{ color: '#000' }}>Calories Burned</div>
            <input
              type="number"
              value={formData.calories_burned ?? ''}
              onChange={(e) => handleChange('calories_burned', Number(e.target.value))}
              min={0}
              style={{
                width: '100%',
                padding: '0.5rem',
                borderRadius: '0.375rem',
                border: '1px solid #cbd5e1',
                background: '#ffffff',
                color: '#000000',
              }}
            />
          </label>

          <label className="block">
            <div className="font-semibold text-sm mb-1" style={{ color: '#000' }}>Perceived Effort (1–10)</div>
            <input
              type="number"
              value={formData.perceived_effort ?? 5}
              onChange={(e) => handleChange('perceived_effort', Number(e.target.value))}
              min={1}
              max={10}
              style={{
                width: '100%',
                padding: '0.5rem',
                borderRadius: '0.375rem',
                border: '1px solid #cbd5e1',
                background: '#ffffff',
                color: '#000000',
              }}
            />
          </label>

          <label className="block">
            <div className="font-semibold text-sm mb-1" style={{ color: '#000' }}>Weight</div>
            <input
              type="number"
              value={formData.weight ?? ''}
              onChange={(e) => handleChange('weight', Number(e.target.value))}
              min={0}
              style={{
                width: '100%',
                padding: '0.5rem',
                borderRadius: '0.375rem',
                border: '1px solid #cbd5e1',
                background: '#ffffff',
                color: '#000000',
              }}
            />
          </label>

          <label className="block">
            <div className="font-semibold text-sm mb-1" style={{ color: '#000' }}>Extra Data (JSON)</div>
            <textarea
              rows={3}
              value={JSON.stringify(formData.exercise_data ?? {}, null, 2)}
              onChange={(e) => {
                try {
                  handleChange('exercise_data', JSON.parse(e.target.value));
                } catch {
                  // ignore parse errors while typing
                }
              }}
              style={{
                width: '100%',
                padding: '0.5rem',
                borderRadius: '0.375rem',
                border: '1px solid #cbd5e1',
                background: '#ffffff',
                color: '#000000',
                fontFamily: 'monospace',
                fontSize: '0.9rem',
              }}
            />
          </label>

          <div className="flex justify-end space-x-2 mt-4">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 rounded bg-gray-300 text-black hover:bg-gray-400 font-semibold"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700 font-semibold"
              disabled={loading}
            >
              {loading ? 'Saving...' : 'Save Workout'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
