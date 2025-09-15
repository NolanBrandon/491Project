import { useState } from "react"
import { supabase } from "../supabaseClient"

export default function Authentication({ setUser }) {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [message, setMessage] = useState("")

  async function handleSignup() {
    const { data, error } = await supabase.auth.signUp({ email, password })
    if (error) setMessage("Error: " + error.message)
    else setMessage("Signup successful! Check your email to confirm.")
  }

  async function handleLogin() {
    const { data, error } = await supabase.auth.signInWithPassword({ email, password })
    if (error) setMessage("Error: " + error.message)
    else setMessage("Login successful!")
  }

  return (
    <div style={{ padding: "20px" }}>
      <h1>Fitness App</h1>
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <br /><br />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <br /><br />
      <button onClick={handleSignup}>Sign Up</button>
      <button onClick={handleLogin} style={{ marginLeft: "10px" }}>Log In</button>
      <p>{message}</p>
    </div>
  )
}
