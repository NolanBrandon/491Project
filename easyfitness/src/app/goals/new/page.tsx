'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import { createGoal, CreateGoalData } from '@/lib/goalsApi';

export default function NewGoalPage() {
  const router = useRouter();
  const { isAuthenticated } = useAuth();

  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [goalType, setGoalType] = useState('');
  const [targetDate, setTargetDate] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  // Redirect if not authenticated
  if (!isAuthenticated) {
    router.replace('/login');
    return null;
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const newGoal: CreateGoalData = {
        title,
        description: description || undefined,
        goal_type: goalType || undefined,
        target_date: targetDate || undefined,
        status: 'active', // default
      };

      await createGoal(newGoal);
      router.push('/dashboard');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create goal');
      console.error('Create goal error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-container blur-bg min-h-screen flex flex-col items-center justify-center p-4">
      <div className="max-w-md w-full bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold mb-4 text-gray-900">Create New Goal</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="text"
            placeholder="Title"
            value={title}
            onChange={e => setTitle(e.target.value)}
            required
            className="w-full border border-gray-300 p-3 rounded text-gray-900 placeholder-gray-400 text-base focus:outline-none focus:ring-2 focus:ring-blue-600"
          />
          <textarea
            placeholder="Description"
            value={description}
            onChange={e => setDescription(e.target.value)}
            className="w-full border border-gray-300 p-3 rounded text-gray-900 placeholder-gray-400 text-base focus:outline-none focus:ring-2 focus:ring-blue-600"
          />
          <input
            type="text"
            placeholder="Goal Type (e.g., Weight Loss, Strength)"
            value={goalType}
            onChange={e => setGoalType(e.target.value)}
            className="w-full border border-gray-300 p-3 rounded text-gray-900 placeholder-gray-400 text-base focus:outline-none focus:ring-2 focus:ring-blue-600"
          />
          <input
            type="date"
            value={targetDate}
            onChange={e => setTargetDate(e.target.value)}
            className="w-full border border-gray-300 p-3 rounded text-gray-900 placeholder-gray-400 text-base focus:outline-none focus:ring-2 focus:ring-blue-600"
          />
          {error && <p className="text-red-600 font-medium">{error}</p>}
          <button
            type="submit"
            className={`w-full py-3 rounded text-white font-semibold text-base ${
              loading ? 'bg-gray-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'
            }`}
            disabled={loading}
          >
            {loading ? 'Creating…' : 'Create Goal'}
          </button>
        </form>
      </div>
    </div>
  );
}
