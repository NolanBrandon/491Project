'use client';

import { useState } from 'react';
import Nav from '../components/navbar';
import Footer from '../components/footer';
import { useRouter } from 'next/navigation';
import { supabase } from '../../lib/supabaseClient';

export default function SignupPage() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [passwordConfirm, setPasswordConfirm] = useState('');
  const [gender, setGender] = useState('');
  const [dateOfBirth, setDateOfBirth] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isSigningUp, setIsSigningUp] = useState(true); // toggle between signup/login
  const [message, setMessage] = useState('');
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setMessage('');

    try {
      if (isSigningUp) {
        if (password !== passwordConfirm) {
          setMessage('Passwords do not match');
          setIsLoading(false);
          return;
        }

        const { data, error } = await supabase.auth.signUp({
          email,
          password,
        });

        if (error) {
          setMessage('Sign up failed: ' + error.message);
        } else {
          setMessage('Sign up successful! Please log in.');
          setIsSigningUp(false);
        }
      } else {
        const { data, error } = await supabase.auth.signInWithPassword({
          email,
          password,
        });

        if (error) {
          setMessage('Login failed: ' + error.message);
        } else {
          setMessage('Login successful!');
          router.push('/mylog');
        }
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
            <h2 className="text-2xl font-bold tracking-wide">
              {isSigningUp ? 'Sign up' : 'Sign in'}
            </h2>
            <p className="auth-muted">
              {isSigningUp ? 'Create a new account' : 'Welcome back'}
            </p>
          </div>

          <form className="space-y-5" onSubmit={handleSubmit}>
            {isSigningUp && (
              <>
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
                  placeholder="Email"
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
                <input
                  type="password"
                  placeholder="Confirm Password"
                  value={passwordConfirm}
                  onChange={(e) => setPasswordConfirm(e.target.value)}
                  required
                  className="auth-input w-full px-3 py-2 rounded-md text-sm"
                />
                <input
                  type="text"
                  placeholder="Gender"
                  value={gender}
                  onChange={(e) => setGender(e.target.value)}
                  required
                  className="auth-input w-full px-3 py-2 rounded-md text-sm"
                />
                <input
                  type="date"
                  placeholder="Date of Birth"
                  value={dateOfBirth}
                  onChange={(e) => setDateOfBirth(e.target.value)}
                  required
                  className="auth-input w-full px-3 py-2 rounded-md text-sm"
                />
              </>
            )}

            {!isSigningUp && (
              <>
                <input
                  type="email"
                  placeholder="Email"
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
              </>
            )}

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

            {message && <p className="text-center text-sm auth-muted mt-2">{message}</p>}

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
