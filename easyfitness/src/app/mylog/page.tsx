'use client';

import { useEffect, useState } from 'react';
import { supabase } from '../../lib/supabaseClient';
import ClientWrapper from '../ClientWrapper';

interface NutritionLog {
  id: string;
  date_eaten: string;
  meal_type: string;
  food_name: string;
  quantity: number;
}

export default function MyLogPage() {
  const [logs, setLogs] = useState<NutritionLog[]>([]);
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

      const { data, error } = await supabase
        .from('nutrition_log')
        .select('*')
        .eq('user_id', user.id)
        .order('date_eaten', { ascending: false });

      if (error) {
        setMessage('Error loading meals: ' + error.message);
      } else {
        setLogs(data || []);
      }
      setLoading(false);
    };

    fetchLogs();
  }, []);

  return (
    <ClientWrapper>
      <h1 className="h1 text-center mb-6">My Nutrition Log</h1>

      {loading ? (
        <p className="auth-muted text-center">Loading meals...</p>
      ) : message ? (
        <p className="auth-muted text-center">{message}</p>
      ) : logs.length === 0 ? (
        <p className="auth-muted text-center">No meals logged yet.</p>
      ) : (
        <div className="space-y-4">
          {logs.map((log) => (
            <div
              key={log.id}
              className="auth-card p-4 border rounded-xl shadow-md bg-white"
            >
              <p>
                <strong>Food:</strong> {log.food_name}
              </p>
              <p>
                <strong>Meal Type:</strong> {log.meal_type}
              </p>
              <p>
                <strong>Quantity:</strong> {log.quantity}
              </p>
              <p>
                <strong>Date:</strong>{' '}
                {new Date(log.date_eaten).toLocaleString()}
              </p>
            </div>
          ))}
        </div>
      )}
    </ClientWrapper>
  );
}
