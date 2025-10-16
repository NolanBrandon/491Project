/**
 * Authentication Context Provider
 * Manages user session state across the application
 */
'use client';

import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { getSessionUser, login as apiLogin, logout as apiLogout, register as apiRegister } from '@/lib/authApi';

interface User {
  id: string;
  username: string;
  email: string;
  gender?: string;
  date_of_birth?: string;
  last_login_date?: string;
  login_streak?: number;
  created_at?: string;
}

interface RegisterData {
  username: string;
  email: string;
  password: string;
  password_confirm: string;
  gender?: string;
  date_of_birth?: string;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (username: string, password: string) => Promise<void>;
  register: (data: RegisterData) => Promise<void>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  /**
   * Refresh user data from session
   */
  const refreshUser = useCallback(async () => {
    try {
      const sessionUser = await getSessionUser();
      setUser(sessionUser);
    } catch (error) {
      console.error('Error refreshing user:', error);
      setUser(null);
    } finally {
      setLoading(false);
    }
  }, []);

  /**
   * Check session on mount
   */
  useEffect(() => {
    refreshUser();
  }, [refreshUser]);

  /**
   * Periodic session validation (every 5 minutes)
   * Helps detect session expiry and keeps session alive
   */
  useEffect(() => {
    if (!user) return;

    const interval = setInterval(async () => {
      try {
        const sessionUser = await getSessionUser();
        if (!sessionUser && user) {
          // Session expired
          console.log('Session expired, logging out...');
          setUser(null);
        } else if (sessionUser) {
          // Update user data if changed
          setUser(sessionUser);
        }
      } catch (error) {
        console.error('Session validation error:', error);
      }
    }, 5 * 60 * 1000); // 5 minutes

    return () => clearInterval(interval);
  }, [user]);

  /**
   * Login function
   */
  const login = async (username: string, password: string) => {
    try {
      const response = await apiLogin(username, password);
      setUser(response.user);
    } catch (error) {
      throw error;
    }
  };

  /**
   * Register function
   */
  const register = async (data: RegisterData) => {
    try {
      const response = await apiRegister(data);
      setUser(response.user);
    } catch (error) {
      throw error;
    }
  };

  /**
   * Logout function
   */
  const logout = async () => {
    try {
      await apiLogout();
      setUser(null);
    } catch (error) {
      // Even if logout fails on server, clear local state
      console.error('Logout API error (still clearing local state):', error);
      setUser(null);
      // Don't re-throw - we want logout to succeed locally even if API fails
    }
  };

  const value: AuthContextType = {
    user,
    loading,
    login,
    register,
    logout,
    refreshUser,
    isAuthenticated: !!user,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

/**
 * Hook to use auth context
 */
export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
