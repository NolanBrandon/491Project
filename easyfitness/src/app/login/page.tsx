'use client';

import { useState } from 'react';
import Nav from '../components/navbar';
import Footer from '../components/footer';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setTimeout(() => {
      console.log('Login attempt:', { email, password });
      setIsLoading(false);
    }, 1000);
  };

  return (
    <div className="page-container blur-bg">
      <Nav />
      <div className="content-grow flex items-center justify-center px-4 py-12">
        <div className="auth-card space-y-8">
          <div className="text-center space-y-2">
            <h2 className="text-2xl font-bold tracking-wide">Sign in to your account</h2>
            <p className="auth-muted">Welcome back to EasyFitness</p>
          </div>
          <form className="space-y-5" onSubmit={handleSubmit}>
            <div className="space-y-4">
              <div className="space-y-1">
                <label htmlFor="email" className="sr-only">Email</label>
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
                <label htmlFor="password" className="sr-only">Password</label>
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
              <a href="#" className="auth-link">Forgot password?</a>
            </div>
            <button
              type="submit"
              disabled={isLoading}
              className="auth-btn w-full py-2.5 rounded-md text-sm text-white transition disabled:cursor-not-allowed"
            >
              {isLoading ? 'Signing in…' : 'Sign In'}
            </button>
            <div className="text-center text-xs auth-muted">
              Don&apos;t have an account? <a href="#" className="auth-link">Sign up</a>
            </div>
          </form>
        </div>
      </div>
      <Footer />
    </div>
  );
}
