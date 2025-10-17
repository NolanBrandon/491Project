'use client';

import { useState, useEffect, use } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import { getGoal, updateGoal, Goal } from '@/lib/goalsApi';

interface GoalDetailsPageProps {
  params: Promise<{ id: string }>; // Next.js App Router now gives a Promise
}

export default function GoalDetailsPage({ params }: GoalDetailsPageProps) {
  const router = useRouter();
  const { isAuthenticated, loading: authLoading } = useAuth();

  // Unwrap the promise to safely access the id
  const { id } = use(params);

  const [goal, setGoal] = useState<Goal | null>(null);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [goalType, setGoalType] = useState('');
  const [targetDate, setTargetDate] = useState('');
  const [status, setStatus] = useState<'active' | 'completed' | 'paused'>('active');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!isAuthenticated) {
      router.replace('/login');
      return;
    }

    const fetchGoal = async () => {
      try {
        const data = await getGoal(id);
        setGoal(data);
        setTitle(data.title);
        setDescription(data.description || '');
        setGoalType(data.goal_type || '');
        setTargetDate(data.target_date || '');
        setStatus(data.status);
      } catch (err) {
        console.error('Error fetching goal:', err);
        setError('Failed to load goal');
      }
    };

    fetchGoal();
  }, [id, isAuthenticated, router]);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      if (!goal) return;

      await updateGoal(goal.id, {
        title,
        description,
        goal_type: goalType,
        target_date: targetDate || undefined,
        status,
      });

      router.push('/dashboard');
    } catch (err) {
      console.error('Error updating goal:', err);
      setError(err instanceof Error ? err.message : 'Failed to update goal');
    } finally {
      setLoading(false);
    }
  };

  if (authLoading) {
    return (
      <div className="page-container blur-bg min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading goal...</p>
        </div>
      </div>
    );
  }

  if (!goal) {
    return null;
  }

  return (
    <div className="page-container blur-bg min-h-screen flex flex-col items-center justify-center p-4">
      <div className="max-w-md w-full bg-white rounded-lg shadow p-6" style={{ color: '#000' }}>
        <h2 className="text-2xl font-bold mb-4 text-gray-900">Edit Goal</h2>
        <form onSubmit={handleSave} className="space-y-4">
          <div>
            <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
              Title *
            </label>
            <input
              id="title"
              type="text"
              placeholder="Enter goal title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
              className="w-full border border-gray-300 p-3 rounded text-gray-900 placeholder-gray-400 text-base focus:outline-none focus:ring-2 focus:ring-blue-600"
            />
          </div>
          <div>
            <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
              Description
            </label>
            <textarea
              id="description"
              placeholder="Enter goal description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              rows={3}
              className="w-full border border-gray-300 p-3 rounded text-gray-900 placeholder-gray-400 text-base focus:outline-none focus:ring-2 focus:ring-blue-600"
            />
          </div>
          <div>
            <label htmlFor="goalType" className="block text-sm font-medium text-gray-700 mb-1">
              Goal Type
            </label>
            <input
              id="goalType"
              type="text"
              placeholder="e.g., Weight Loss, Strength, Endurance"
              value={goalType}
              onChange={(e) => setGoalType(e.target.value)}
              className="w-full border border-gray-300 p-3 rounded text-gray-900 placeholder-gray-400 text-base focus:outline-none focus:ring-2 focus:ring-blue-600"
            />
          </div>
          <div>
            <label htmlFor="targetDate" className="block text-sm font-medium text-gray-700 mb-1">
              Target Date
            </label>
            <input
              id="targetDate"
              type="date"
              value={targetDate}
              onChange={(e) => setTargetDate(e.target.value)}
              className="w-full border border-gray-300 p-3 rounded text-gray-900 placeholder-gray-400 text-base focus:outline-none focus:ring-2 focus:ring-blue-600"
            />
          </div>
          <div>
            <label htmlFor="status" className="block text-sm font-medium text-gray-700 mb-1">
              Status
            </label>
            <select
              id="status"
              value={status}
              onChange={(e) => setStatus(e.target.value as 'active' | 'completed' | 'paused')}
              className="w-full border border-gray-300 p-3 rounded text-gray-900 text-base focus:outline-none focus:ring-2 focus:ring-blue-600"
            >
              <option value="active">Active</option>
              <option value="completed">Completed</option>
              <option value="paused">Paused</option>
            </select>
          </div>
          {error && <p className="text-red-600">{error}</p>}
          <button
            type="submit"
            className={`w-full py-2 rounded text-white ${
              loading ? 'bg-gray-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'
            }`}
            disabled={loading}
          >
            {loading ? 'Saving…' : 'Save Changes'}
          </button>
        </form>
      </div>
    </div>
  );
}
