"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { createClientComponentClient } from "@supabase/auth-helpers-nextjs";


export default function NutritionPage() {
  const supabase = createClientComponentClient();
  const router = useRouter();

  const [entries, setEntries] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadEntries() {
      const {
        data: { user },
      } = await supabase.auth.getUser();
      if (!user) {
        router.push("/login");
        return;
      }

      const { data, error } = await supabase
        .from("nutrition_log")
        .select("*")
        .eq("user_id", user.id)
        .order("created_at", { ascending: false });

      if (!error) {
        setEntries(data || []);
      }

      setLoading(false);
    }

    loadEntries();
  }, []);

  async function handleDelete(id: string) {
    await supabase.from("nutrition_log").delete().eq("id", id);
    router.refresh();
  }

  if (loading) return <p>Loading...</p>;

  const totalCalories = entries.reduce(
    (acc, item) => acc + Number(item.calories || 0),
    0
  );

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Nutrition Log</h1>

      <button
        onClick={() => router.push("/Nutrition/new")}
        className="mb-4 px-4 py-2 bg-green-600 text-white rounded"
      >
        Add New Entry
      </button>

      {entries.length === 0 ? (
        <p>No entries yet.</p>
      ) : (
        <div className="space-y-4">
          {entries.map((entry) => (
            <div
              key={entry.id}
              className="border p-4 rounded flex justify-between items-center"
            >
              <div>
                <h2 className="font-semibold">{entry.food_name}</h2>
                <p>Calories: {entry.calories}</p>
                <p>
                  Serving Size: {entry.serving_size} •{" "}
                  {new Date(entry.created_at).toLocaleString()}
                </p>
              </div>

              <div className="space-x-2">
                <button
                  onClick={() =>
                    router.push(`/Nutrition/new?edit=${entry.id}`)
                  }
                  className="px-3 py-1 bg-yellow-500 text-white rounded"
                >
                  Edit
                </button>

                <button
                  onClick={() => handleDelete(entry.id)}
                  className="px-3 py-1 bg-red-600 text-white rounded"
                >
                  Delete
                </button>
              </div>
            </div>
          ))}

          <div className="mt-4 p-4 bg-gray-100 rounded font-bold">
            Total Calories Today: {totalCalories}
          </div>
        </div>
      )}
    </div>
  );
}
