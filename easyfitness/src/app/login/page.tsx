'use client';

import { useState } from 'react';
import Nav from '../components/navbar';
import Footer from '../components/footer';
import { useRouter } from 'next/navigation';

export default function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();
  const [message, setMessage] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setMessage('');

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/users/login/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();

      if (!response.ok) {
        setMessage('Login failed: ' + (data.error || JSON.stringify(data)));
      } else {
        setMessage('Login successful!');
        // Redirect to dashboard or main page
        router.push(`/users/${data.user.id}/dashboard/`);
      }
    } catch (err) {
      setMessage('Unexpected error: ' + (err as Error).message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="page-container blur-bg min-h-screen flex flex-col">
      <Nav />
      <div className="content-grow flex items-center justify-center px-4 py-12 flex-1">
        <div className="auth-card space-y-8">
          <div className="text-center space-y-2">
            <h2 className="text-2xl font-bold tracking-wide">Sign in to your account</h2>
            <p className="auth-muted">Welcome back to EasyFitness</p>
          </div>

          <form className="space-y-5" onSubmit={handleSubmit}>
            <div className="space-y-4">
              <input
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                className="auth-input w-full px-3 py-2 rounded-md text-sm"
              />
              <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="auth-input w-full px-3 py-2 rounded-md text-sm"
              />
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="auth-btn w-full py-2.5 rounded-md text-sm text-white transition disabled:cursor-not-allowed"
            >
              {isLoading ? 'Signing in…' : 'Sign In'}
            </button>

            {message && <p className="text-center text-sm auth-muted mt-2">{message}</p>}
          </form>
        </div>
      </div>
      <Footer />
    </div>
  );
}
