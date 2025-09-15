import { useState } from "react"
import { supabase } from "../supabaseClient"

export default function AddDiet({ user }) {
  const [name, setName] = useState("")
  const [calories, setCalories] = useState("")
  const [message, setMessage] = useState("")

  async function handleAddDiet() {
    if (!name || !calories) {
      setMessage("Please enter both name and calories.")
      return
    }

    const { data, error } = await supabase
      .from("diets")
      .insert([
        { user_id: user.id, name, calories: parseInt(calories) }
      ])

    if (error) setMessage("Error: " + error.message)
    else {
      setMessage("Diet added successfully!")
      setName("")
      setCalories("")
    }
  }

  return (
    <div style={{ marginTop: "20px" }}>
      <h2>Add Diet</h2>
      <input
        type="text"
        placeholder="Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <br /><br />
      <input
        type="number"
        placeholder="Calories"
        value={calories}
        onChange={(e) => setCalories(e.target.value)}
      />
      <br /><br />
      <button onClick={handleAddDiet}>Save Diet</button>
      <p>{message}</p>
    </div>
  )
}
