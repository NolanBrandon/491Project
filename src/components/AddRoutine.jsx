import { useState } from "react"
import { supabase } from "../supabaseClient"

export default function AddRoutine({ user }) {
  const [title, setTitle] = useState("")
  const [description, setDescription] = useState("")
  const [message, setMessage] = useState("")

  async function handleAddRoutine() {
    if (!title) {
      setMessage("Please enter a title.")
      return
    }

    const { data, error } = await supabase
      .from("routines")
      .insert([
        { user_id: user.id, title, description }
      ])

    if (error) setMessage("Error: " + error.message)
    else {
      setMessage("Routine added successfully!")
      setTitle("")
      setDescription("")
    }
  }

  return (
    <div style={{ marginTop: "20px" }}>
      <h2>Add Routine</h2>
      <input
        type="text"
        placeholder="Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />
      <br /><br />
      <textarea
        placeholder="Description"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />
      <br /><br />
      <button onClick={handleAddRoutine}>Save Routine</button>
      <p>{message}</p>
    </div>
  )
}
