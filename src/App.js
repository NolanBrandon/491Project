import React, { useState, useEffect } from "react";
import { auth } from "./firebase";
import { 
  createUserWithEmailAndPassword, 
  signInWithEmailAndPassword, 
  signOut,
  onAuthStateChanged
} from "firebase/auth";

function App() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [user, setUser] = useState(null); // Logged-in user

  // Track auth state
  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser);
    });
    return () => unsubscribe();
  }, []);

  // Sign up new user
  const handleSignup = async () => {
    try {
      await createUserWithEmailAndPassword(auth, email, password);
      alert("User created! Logged in automatically.");
      setEmail("");
      setPassword("");
    } catch (err) {
      alert(err.message);
    }
  };

  // Login existing user
  const handleLogin = async () => {
    try {
      await signInWithEmailAndPassword(auth, email, password);
      setEmail("");
      setPassword("");
    } catch (err) {
      alert(err.message);
    }
  };

  // Logout
  const handleLogout = async () => {
    await signOut(auth);
  };

  // If logged in, show Main Menu
  if (user) {
    return (
      <div style={{ padding: "20px" }}>
        <h1>Welcome, {user.email}</h1>
        <h2>Main Menu</h2>
        <ul>
          <li>Workout Plans</li>
          <li>Progress Tracker</li>
          <li>Profile</li>
        </ul>
        <button onClick={handleLogout}>Logout</button>
      </div>
    );
  }

  // Otherwise show login/signup form
  return (
    <div style={{ padding: "20px" }}>
      <h1>Fitness App</h1>
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        style={{ display: "block", marginBottom: "10px" }}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        style={{ display: "block", marginBottom: "10px" }}
      />
      <button onClick={handleSignup}>Sign Up</button>
      <button onClick={handleLogin} style={{ marginLeft: "10px" }}>
        Login
      </button>
    </div>
  );
}

export default App;
