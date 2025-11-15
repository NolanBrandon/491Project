'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import {
  getNutritionLogs,
  deleteNutritionLog,
  NutritionLog,
} from '@/lib/nutritionApi';

export default function NutritionPage() {
  const router = useRouter();
  const { isAuthenticated } = useAuth();

  const [logs, setLogs] = useState<NutritionLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Redirect if not authenticated
  if (!isAuthenticated) {
    router.replace('/login');
    return null;
  }

  // Fetch logs
  const fetchLogs = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getNutritionLogs();
      setLogs(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch nutrition logs');
      console.error('Fetch logs error:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLogs();
  }, []);

  // Delete log
  const handleDelete = async (id: string) => {
    try {
      await deleteNutritionLog(id);
      // Refresh list after deletion
      setLogs(prev => prev.filter(log => log.id !== id));
    } catch (err) {
      console.error('Delete log error:', err);
      setError(err instanceof Error ? err.message : 'Failed to delete log');
    }
  };

  return (
    <div className="page-container blur-bg min-h-screen flex flex-col items-center justify-center p-4">
      <div className="max-w-md w-full bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold mb-4 text-gray-900">Nutrition Logs</h2>

        {error && <p className="text-red-600 font-medium mb-4">{error}</p>}

        {loading ? (
          <p>Loading...</p>
        ) : logs.length === 0 ? (
          <p>No nutrition logs found.</p>
        ) : (
          <ul className="space-y-4">
            {logs.map(log => (
              <li
                key={log.id}
                className="border border-gray-300 p-3 rounded flex justify-between items-center"
              >
                <div>
                  <p className="font-semibold">{log.food_name}</p>
                  <p className="text-sm text-gray-600">{log.meal_type}</p>
                  <p className="text-sm text-gray-600">
                    {log.calories ?? 0} calories | {log.protein ?? 0} g protein
                  </p>
                </div>
                <button
                  onClick={() => handleDelete(log.id)}
                  className="text-red-600 font-medium hover:underline"
                >
                  Delete
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
