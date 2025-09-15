import { useState, useEffect } from "react"
import Authentication from "./components/Authentication"
import MainMenu from "./components/MainMenu"
import { supabase } from "./supabaseClient"

function App() {
  const [user, setUser] = useState(null)

  // Check if user is logged in
  useEffect(() => {
    supabase.auth.getSession().then(({ data }) => {
      setUser(data.session?.user ?? null)
    })

    const { data: listener } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user ?? null)
    })

    return () => listener.subscription.unsubscribe()
  }, [])

  return user ? <MainMenu user={user} setUser={setUser} /> : <Authentication setUser={setUser} />
}

export default App
