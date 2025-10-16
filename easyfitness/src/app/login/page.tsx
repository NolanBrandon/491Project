'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import Nav from '../components/navbar';
import Footer from '../components/footer';
import { useRouter } from 'next/navigation';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isSigningUp, setIsSigningUp] = useState(false);
  const [message, setMessage] = useState('');
  const router = useRouter();
  const { login, isAuthenticated, loading: authLoading } = useAuth();

  // Redirect to dashboard if already authenticated
  useEffect(() => {
    if (!authLoading && isAuthenticated) {
      console.log('Already authenticated, redirecting to dashboard');
      router.replace('/dashboard');
    }
  }, [authLoading, isAuthenticated, router]);

  // Show loading while checking auth
  if (authLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  // Don't render form if authenticated (will redirect via useEffect)
  if (isAuthenticated) {
    return null;
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setMessage('');

    try {
      if (isSigningUp) {
        setMessage('Please use the Sign Up page for registration');
        setIsLoading(false);
        return;
      }
      
      // Login using Django backend
      // For Django, we use username, but user enters email
      // We'll use email as username for now
      await login(email, password);
      setMessage('Login successful! Redirecting...');
      console.log('Login successful, redirecting to dashboard');
      // Redirect after successful login
      router.replace('/dashboard');
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Login failed';
      setMessage(errorMessage);
      console.error('Login error:', errorMessage);
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
            <h2 className="text-2xl font-bold tracking-wide">
  {isSigningUp ? 'Create your account' : 'Sign in to your account'}
</h2>

            <p className="auth-muted">Welcome back to EasyFitness</p>
          </div>

          <form className="space-y-5" onSubmit={handleSubmit}>
            <div className="space-y-4">
              <input
                type="text"
                placeholder="Username or Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
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
              {isLoading
                ? isSigningUp
                  ? 'Signing up…'
                  : 'Signing in…'
                : isSigningUp
                ? 'Sign Up'
                : 'Sign In'}
            </button>

            {message && (
              <p className="text-center text-sm auth-muted mt-2">{message}</p>
            )}

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
