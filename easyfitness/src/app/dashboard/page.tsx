'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import { getGoals, Goal, deleteGoal } from '@/lib/goalsApi';
import Nav from '../components/navbar';
import Footer from '../components/footer';

export default function DashboardPage() {
  const router = useRouter();
  const { user, isAuthenticated, loading: authLoading } = useAuth();
  const [goals, setGoals] = useState<Goal[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [hasFetched, setHasFetched] = useState(false);
  const [goalToDelete, setGoalToDelete] = useState<Goal | null>(null);
  const [showDeleteModal, setShowDeleteModal] = useState(false);

  // Redirect to login if not authenticated after auth check completes
  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.replace('/login');
    }
  }, [authLoading, isAuthenticated, router]);

  // Fetch dashboard data only when authenticated
  useEffect(() => {
    if (!authLoading && isAuthenticated && !hasFetched) {
      setHasFetched(true);
      fetchDashboardData();
    }
  }, [authLoading, isAuthenticated, hasFetched]);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);
      const goalsData = await getGoals();
      setGoals(goalsData);
    } catch (err) {
      console.error('Error fetching dashboard data:', err);
      setError('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteGoal = async (goalId: string) => {
    try {
      await deleteGoal(goalId);
      setGoals(goals.filter((g) => g.id !== goalId));
    } catch (err) {
      console.error('Error deleting goal:', err);
      alert('Failed to delete goal');
    }
  };

  const formatDate = (dateString: string | null) => {
    if (!dateString) return 'No date set';
    return new Date(dateString).toLocaleDateString();
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'bg-green-100 text-green-800';
      case 'completed':
        return 'bg-blue-100 text-blue-800';
      case 'paused':
        return 'bg-gray-100 text-gray-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  if (authLoading || (isAuthenticated && loading)) {
    return (
      <div className="page-container blur-bg min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) return null;

  return (
    <div className="page-container blur-bg min-h-screen flex flex-col">
      <Nav />

      {/* Header */}
      <div className="bg-white/80 backdrop-blur-sm shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="text-3xl font-bold text-gray-900">
            Welcome back, {user?.username || 'User'}!
          </h1>
          <p className="mt-2 text-gray-600">
            Here's an overview of your fitness journey
          </p>
        </div>
      </div>

      <div className="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 w-full">
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
            {error}
          </div>
        )}

        {/* Goals Section */}
        <div className="mb-8">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-2xl font-bold text-gray-900">Your Goals</h2>
            <button
              onClick={() => router.push('/goals/new')}
              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md font-medium transition-colors"
            >
              + Create New Goal
            </button>
          </div>

          {goals.length === 0 ? (
            <div className="bg-white rounded-lg shadow p-8 text-center">
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                No goals yet
              </h3>
              <p className="text-gray-600 mb-4">
                Start your fitness journey by creating your first goal!
              </p>
              <button
                onClick={() => router.push('/goals/new')}
                className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-md font-medium transition-colors"
              >
                Create Your First Goal
              </button>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {goals.map((goal) => (
                <div
                  key={goal.id}
                  className="bg-white rounded-lg shadow hover:shadow-md transition-shadow p-6 flex flex-col justify-between"
                >
                  <div className="flex justify-between items-start mb-3">
                    <h3 className="text-lg font-semibold flex-1 !text-black">
                      {goal.title}
                    </h3>
                    <span
                      className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(
                        goal.status
                      )}`}
                    >
                      {goal.status}
                    </span>
                  </div>

                  <p className="text-gray-700 text-sm mb-4 line-clamp-2 break-words">
                    {goal.description || 'No description'}
                  </p>

                  <div className="space-y-1 text-sm text-gray-600 mb-4">
                    {goal.goal_type && (
                      <div className="flex items-center">
                        <span className="font-medium mr-2">Type:</span>
                        {goal.goal_type}
                      </div>
                    )}
                    {goal.target_date && (
                      <div className="flex items-center">
                        <span className="font-medium mr-2">Target:</span>
                        {formatDate(goal.target_date)}
                      </div>
                    )}
                  </div>

                  <div className="flex space-x-2 mt-auto">
                    <button
                      onClick={() => router.push(`/goals/${goal.id}`)}
                      className="flex-1 bg-blue-50 hover:bg-blue-100 text-blue-700 px-3 py-2 rounded text-sm font-medium transition-colors"
                    >
                      View Details
                    </button>
                    <button
                      onClick={() => {
                        setGoalToDelete(goal);
                        setShowDeleteModal(true);
                      }}
                      className="bg-red-50 hover:bg-red-100 text-red-700 px-3 py-2 rounded text-sm font-medium transition-colors"
                    >
                      Delete
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Modal */}
        {showDeleteModal && goalToDelete && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 shadow-lg max-w-sm w-full">
              <h3 className="text-lg font-bold text-gray-900 mb-4">
                Delete Goal
              </h3>
              <p className="text-gray-700 mb-6">
                Are you sure you want to delete "<span className="font-semibold">{goalToDelete.title}</span>"? This action cannot be undone.
              </p>
              <div className="flex justify-end space-x-4">
                <button
                  className="px-4 py-2 rounded bg-gray-200 hover:bg-gray-300"
                  onClick={() => setShowDeleteModal(false)}
                >
                  Cancel
                </button>
                <button
                  className="px-4 py-2 rounded bg-red-600 text-white hover:bg-red-700"
                  onClick={async () => {
                    try {
                      await handleDeleteGoal(goalToDelete.id);
                    } finally {
                      setShowDeleteModal(false);
                      setGoalToDelete(null);
                    }
                  }}
                >
                  Delete
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Placeholder Sections */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Workout Plan</h2>
            <div className="text-center py-8 text-gray-400">
              <p>Create and track your workout routines</p>
            </div>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Meal Plan</h2>
            <div className="text-center py-8 text-gray-400">
              <p>Plan your daily meals and nutrition</p>
            </div>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Workout Log</h2>
            <div className="text-center py-8 text-gray-400">
              <p>Log your completed workouts and progress</p>
            </div>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Nutrition Log</h2>
            <div className="text-center py-8 text-gray-400">
              <p>Track your daily food intake and calories</p>
            </div>
          </div>
        </div>
      </div>

      <Footer />
    </div>
  );
}
