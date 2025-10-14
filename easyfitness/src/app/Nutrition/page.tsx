// src/app/nutrition/page.tsx
'use client';

import { useState } from 'react';
import { supabase } from '../../lib/supabaseClient';
import ClientWrapper from '../ClientWrapper';

export default function NutritionPageContent() {
  const [dateEaten, setDateEaten] = useState('');
  const [mealType, setMealType] = useState('Breakfast');
  const [foodName, setFoodName] = useState('');
  const [protein, setProtein] = useState(''); // protein in grams
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setMessage('');

    // Get current user
    const { data: { user } } = await supabase.auth.getUser();
    if (!user) {
      setMessage('You must be logged in to add meals.');
      setIsLoading(false);
      return;
    }

    // Insert into nutrition_log
    const { error } = await supabase.from('nutrition_log').insert({
      date_eaten: dateEaten,
      meal_type: mealType,
      food_name: foodName,
      quantity: parseFloat(protein), // store protein in quantity
      user_id: user.id,
      food_data: { protein: parseFloat(protein) }, // optional: store extra info
    });

    if (error) {
      setMessage('Error adding meal: ' + error.message);
    } else {
      setMessage('Meal added successfully!');
      setDateEaten('');
      setMealType('Breakfast');
      setFoodName('');
      setProtein('');
    }

    setIsLoading(false);
  };

  return (
    <ClientWrapper>
      <h1 className="h1">Add Nutrition</h1>

      <form className="auth-card space-y-4" onSubmit={handleSubmit}>
        <label>
          Date & Time:
          <input
            type="datetime-local"
            value={dateEaten}
            onChange={(e) => setDateEaten(e.target.value)}
            required
            className="auth-input w-full"
          />
        </label>

        <label>
          Meal Type:
          <select
            value={mealType}
            onChange={(e) => setMealType(e.target.value)}
            className="auth-input w-full"
          >
            <option>Breakfast</option>
            <option>Lunch</option>
            <option>Dinner</option>
            <option>Snack</option>
          </select>
        </label>

        <label>
          Food Name:
          <input
            type="text"
            value={foodName}
            onChange={(e) => setFoodName(e.target.value)}
            required
            className="auth-input w-full"
          />
        </label>

        <label>
          Protein (grams):
          <input
            type="number"
            value={protein}
            onChange={(e) => setProtein(e.target.value)}
            required
            className="auth-input w-full"
            step="any"
          />
        </label>

        <button type="submit" className="auth-btn w-full" disabled={isLoading}>
          {isLoading ? 'Adding…' : 'Add Meal'}
        </button>

        {message && <p className="auth-muted text-center">{message}</p>}
      </form>
    </ClientWrapper>
  );
}
