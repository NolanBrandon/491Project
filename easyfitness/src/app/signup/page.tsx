'use client';

import { useState, useEffect } from 'react';
import { supabase } from '../../lib/supabaseClient';
import Nav from '../components/navbar';
import Footer from '../components/footer';
import { useRouter } from 'next/navigation';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isSigningUp, setIsSigningUp] = useState(false);

  const router = useRouter();

  // Check backend health once on mount
  useEffect(() => {
    const checkBackend = async () => {
      try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/health/`);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data = await response.json();
        console.log('Backend health check:', data);
      } catch (err) {
        console.error('Backend connection failed:', err);
      }
    };

    checkBackend();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    if (isSigningUp) {
      // Sign up
      const { data, error } = await supabase.auth.signUp({ email, password });

      setIsLoading(false);

      if (error) {
        alert('Sign up failed: ' + error.message);
      } else {
        alert('Sign up successful! Please check your email to confirm.');
        setIsSigningUp(false);
      }
    } else {
      // Log in
      const { data, error } = await supabase.auth.signInWithPassword({ email, password });

      setIsLoading(false);

      if (error) {
        alert('Login failed: ' + error.message);
      } else if (!data.session) {
        alert('Login failed: no session returned.');
      } else {
        alert('Login successful!');
        router.push('/mylog'); // redirect after login
      }
    }
  };

  return (
    <div className="page-container blur-bg min-h-screen flex flex-col">
      <Nav />
      <div className="content-grow flex items-center justify-center px-4 py-12 flex-1">
        <div className="auth-card space-y-8">
          <div className="text-center space-y-2">
            <h2 className="text-2xl font-bold tracking-wide">
              {isSigningUp ? 'Sign up' : 'Sign in'}
            </h2>
            <p className="auth-muted">
              {isSigningUp
                ? 'Create a new account'
                : 'Welcome back to EasyFitness'}
            </p>
          </div>

          <form className="space-y-5" onSubmit={handleSubmit}>
            <div className="space-y-4">
              <div className="space-y-1">
                <label htmlFor="email" className="sr-only">
                  Email
                </label>
                <input
                  id="email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  className="auth-input w-full px-3 py-2 rounded-md text-sm"
                  placeholder="Email address"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </div>

              <div className="space-y-1">
                <label htmlFor="password" className="sr-only">
                  Password
                </label>
                <input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="current-password"
                  required
                  className="auth-input w-full px-3 py-2 rounded-md text-sm"
                  placeholder="Password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>
            </div>

            <div className="flex items-center justify-between text-xs">
              <label className="inline-flex items-center gap-2 cursor-pointer select-none">
                <input type="checkbox" className="accent-indigo-500" />
                <span className="auth-muted">Remember me</span>
              </label>
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="auth-btn w-full py-2.5 rounded-md text-sm text-white transition disabled:cursor-not-allowed"
            >
              {isLoading ? (isSigningUp ? 'Signing up…' : 'Signing in…') : (isSigningUp ? 'Sign Up' : 'Sign In')}
            </button>

            <div className="text-center text-xs auth-muted">
              {isSigningUp ? (
                <>
                  Already have an account?{' '}
                  <button
                    type="button"
                    className="auth-link"
                    onClick={() => setIsSigningUp(false)}
                  >
                    Sign in
                  </button>
                </>
              ) : (
                <>
                  Don&apos;t have an account?{' '}
                  <button
                    type="button"
                    className="auth-link"
                    onClick={() => setIsSigningUp(true)}
                  >
                    Sign up
                  </button>
                </>
              )}
            </div>
          </form>
        </div>
      </div>
      <Footer />
    </div>
  );
}
