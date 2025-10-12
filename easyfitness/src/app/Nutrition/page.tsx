// src/app/nutrition/page.tsx
'use client';

import { useState } from 'react';
import { supabase } from '../../lib/supabaseClient';
import ClientWrapper from '../ClientWrapper';

export default function NutritionPageContent() {
  const [dateEaten, setDateEaten] = useState('');
  const [mealType, setMealType] = useState('Breakfast');
  const [foodName, setFoodName] = useState('');
  const [quantity, setQuantity] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setMessage('');

    // Correct v2 syntax to get current user
    const { data: { user } } = await supabase.auth.getUser();
    if (!user) {
      setMessage('You must be logged in to add meals.');
      setIsLoading(false);
      return;
    }

    const { error } = await supabase.from('nutrition_log').insert({
      date_eaten: dateEaten,
      meal_type: mealType,
      food_name: foodName,
      quantity: parseFloat(quantity),
      user_id: user.id, // use current authenticated user
      food_id: null, // allow manual entry
    });

    if (error) {
      setMessage('Error adding meal: ' + error.message);
    } else {
      setMessage('Meal added successfully!');
      setDateEaten('');
      setMealType('Breakfast');
      setFoodName('');
      setQuantity('');
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
          Quantity:
          <input
            type="number"
            value={quantity}
            onChange={(e) => setQuantity(e.target.value)}
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
