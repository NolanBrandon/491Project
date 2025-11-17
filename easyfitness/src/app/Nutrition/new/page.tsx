"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/contexts/AuthContext";
import {
  createNutritionLog,
  CreateNutritionLogData,
} from "@/lib/nutritionApi";
import { useEffect } from "react";


export default function NewNutritionLogPage() {
  const router = useRouter();
  const { isAuthenticated, user } = useAuth();

  const [foodName, setFoodName] = useState("");
  const [mealType, setMealType] = useState("");
  const [calories, setCalories] = useState("");
  const [protein, setProtein] = useState("");
  const [dateEaten, setDateEaten] = useState("");
  const [timeEaten, setTimeEaten] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  // Redirect if not authenticated
  useEffect(() => {
  if (isAuthenticated === false) {
    router.replace("/login");
  }
}, [isAuthenticated, router]);

if (isAuthenticated === false) return null;


  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      // Build datetime safely
      let dateTimeEaten: string;
      if (dateEaten) {
        const [y, m, d] = dateEaten.split("-").map(Number);
        const [hour = 12, minute = 0] = timeEaten.split(":").map(Number);
        const localDate = new Date(y, m - 1, d, hour, minute);
        dateTimeEaten = localDate.toISOString();
      } else {
        dateTimeEaten = new Date().toISOString();
      }

      const newLog: CreateNutritionLogData = {
        food_name: foodName.trim(),
        meal_type: mealType.trim(),
        calories: calories ? Number(calories) : undefined,
        protein: protein ? Number(protein) : undefined,
        date_eaten: dateTimeEaten,
        quantity: 0,
        user: user?.id,
      };

      await createNutritionLog(newLog);

      // Reset form
      setFoodName("");
      setMealType("");
      setCalories("");
      setProtein("");
      setDateEaten("");
      setTimeEaten("");

      router.push("/dashboard");
    } catch (err) {
      console.error("Create nutrition log error:", err);
      setError(
        err instanceof Error
          ? err.message
          : "Failed to create nutrition log"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-container blur-bg min-h-screen flex flex-col items-center justify-center p-4">
      <div className="max-w-md w-full bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold mb-4 text-gray-900">
          Add Nutrition Log
        </h2>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label
              htmlFor="foodName"
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              Food Name *
            </label>
            <input
              id="foodName"
              type="text"
              placeholder="e.g., Chicken Salad"
              value={foodName}
              onChange={(e) => setFoodName(e.target.value)}
              required
              className="w-full border border-gray-300 p-3 rounded text-gray-900 placeholder-gray-400 text-base focus:outline-none focus:ring-2 focus:ring-green-600"
            />
          </div>

          <div>
            <label
              htmlFor="mealType"
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              Meal Type
            </label>
            <select
              id="mealType"
              value={mealType}
              onChange={(e) => setMealType(e.target.value)}
              className="w-full border border-gray-300 p-3 rounded text-gray-900 text-base focus:outline-none focus:ring-2 focus:ring-green-600"
            >
              <option value="">Select meal type</option>
              <option value="breakfast">Breakfast</option>
              <option value="lunch">Lunch</option>
              <option value="dinner">Dinner</option>
              <option value="snack">Snack</option>
            </select>
          </div>

          <div>
            <label
              htmlFor="calories"
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              Calories
            </label>
            <input
              id="calories"
              type="number"
              step="1"
              placeholder="e.g., 350"
              value={calories}
              onChange={(e) => setCalories(e.target.value)}
              className="w-full border border-gray-300 p-3 rounded text-gray-900 placeholder-gray-400 text-base focus:outline-none focus:ring-2 focus:ring-green-600"
            />
          </div>

          <div>
            <label
              htmlFor="protein"
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              Protein (g)
            </label>
            <input
              id="protein"
              type="number"
              step="1"
              placeholder="e.g., 25"
              value={protein}
              onChange={(e) => setProtein(e.target.value)}
              className="w-full border border-gray-300 p-3 rounded text-gray-900 placeholder-gray-400 text-base focus:outline-none focus:ring-2 focus:ring-green-600"
            />
          </div>

          <div className="flex space-x-4">
            <div className="flex-1">
              <label
                htmlFor="dateEaten"
                className="block text-sm font-medium text-gray-700 mb-1"
              >
                Date Eaten
              </label>
              <input
                id="dateEaten"
                type="date"
                value={dateEaten}
                onChange={(e) => setDateEaten(e.target.value)}
                className="w-full border border-gray-300 p-3 rounded text-gray-900 placeholder-gray-400 text-base focus:outline-none focus:ring-2 focus:ring-green-600"
              />
            </div>

            <div className="flex-1">
              <label
                htmlFor="timeEaten"
                className="block text-sm font-medium text-gray-700 mb-1"
              >
                Time Eaten
              </label>
              <input
                id="timeEaten"
                type="time"
                value={timeEaten}
                onChange={(e) => setTimeEaten(e.target.value)}
                className="w-full border border-gray-300 p-3 rounded text-gray-900 placeholder-gray-400 text-base focus:outline-none focus:ring-2 focus:ring-green-600"
              />
            </div>
          </div>

          {error && (
            <p className="text-red-600 font-medium">{error}</p>
          )}

          <button
            type="submit"
            className={`w-full py-3 rounded text-white font-semibold text-base ${
              loading
                ? "bg-gray-400 cursor-not-allowed"
                : "bg-green-600 hover:bg-green-700"
            }`}
            disabled={loading}
          >
            {loading ? "Adding…" : "Add Log"}
          </button>
        </form>
      </div>
    </div>
  );
}
