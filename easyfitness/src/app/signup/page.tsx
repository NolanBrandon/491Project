'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import Nav from '../components/navbar';
import Footer from '../components/footer';
import { useRouter } from 'next/navigation';

export default function SignUpPage() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [passwordConfirm, setPasswordConfirm] = useState('');
  const [gender, setGender] = useState('');
  const [dateOfBirth, setDateOfBirth] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState('');

  const router = useRouter();
  const { register, isAuthenticated, loading: authLoading } = useAuth();

  // Check backend health once on mount
  useEffect(() => {
    const checkBackend = async () => {
      try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/health/`, {
          credentials: 'include'
        });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data = await response.json();
        console.log('Backend health check:', data);
      } catch (err) {
        console.error('Backend connection failed:', err);
      }
    };

    checkBackend();
  }, []);

  // Redirect if already authenticated
  useEffect(() => {
    if (!authLoading && isAuthenticated) {
      router.replace('/dashboard');
    }
  }, [isAuthenticated, authLoading, router]);

  // Don't render form if already authenticated
  if (!authLoading && isAuthenticated) {
    return null;
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setMessage('');

    // Validate passwords match
    if (password !== passwordConfirm) {
      setMessage('Passwords do not match');
      setIsLoading(false);
      return;
    }

    try {
      await register({
        username,
        email,
        password,
        password_confirm: passwordConfirm,
        gender: gender || undefined,
        date_of_birth: dateOfBirth || undefined,
      });
      
      setMessage('Sign up successful! Redirecting...');
      setTimeout(() => router.push('/dashboard'), 1500);
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Sign up failed';
      setMessage(errorMessage);
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
              Create your account
            </h2>
            <p className="auth-muted">
              Join EasyFitness today
            </p>
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
                type="email"
                placeholder="Email address"
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
                minLength={8}
                className="auth-input w-full px-3 py-2 rounded-md text-sm"
              />
              
              <input
                type="password"
                placeholder="Confirm Password"
                value={passwordConfirm}
                onChange={(e) => setPasswordConfirm(e.target.value)}
                required
                minLength={8}
                className="auth-input w-full px-3 py-2 rounded-md text-sm"
              />
              
              <select
                value={gender}
                onChange={(e) => setGender(e.target.value)}
                className="auth-input w-full px-3 py-2 rounded-md text-sm"
              >
                <option value="">Select Gender (Optional)</option>
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="other">Other</option>
              </select>
              
              <input
                type="date"
                placeholder="Date of Birth"
                value={dateOfBirth}
                onChange={(e) => setDateOfBirth(e.target.value)}
                className="auth-input w-full px-3 py-2 rounded-md text-sm"
              />
            </div>

            {message && (
              <p className={`text-center text-sm ${message.includes('successful') ? 'text-green-600' : 'text-red-600'}`}>
                {message}
              </p>
            )}

            <button
              type="submit"
              disabled={isLoading}
              className="auth-btn w-full py-2.5 rounded-md text-sm text-white transition disabled:cursor-not-allowed"
            >
              {isLoading ? 'Signing up…' : 'Sign Up'}
            </button>

            <div className="text-center text-xs auth-muted">
              Already have an account?{' '}
              <a href="/login" className="auth-link">
                Sign in
              </a>
            </div>
          </form>
        </div>
      </div>
      <Footer />
    </div>
  );
}
