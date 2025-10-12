// jest.setup.ts
import '@testing-library/jest-dom';
import { TextEncoder, TextDecoder } from 'util';

// Mock fetch globally
global.fetch = async (input: RequestInfo, init?: RequestInit) => {
  // Default response for backend health check
  if (typeof input === 'string' && input.includes('/health')) {
    return {
      ok: true,
      json: async () => ({ status: 'healthy' }),
    } as Response;
  }
  // Default response for login/sign-up
  if (typeof input === 'string' && input.includes('/auth/v1/token')) {
    return {
      ok: true,
      json: async () => ({ session: { access_token: 'fake-token' } }),
    } as Response;
  }
  return {
    ok: true,
    json: async () => ({}),
  } as Response;
};

// Mock window.alert
global.alert = jest.fn();

// Polyfill for TextEncoder/TextDecoder
global.TextEncoder = TextEncoder;
global.TextDecoder = TextDecoder;

// Provide environment variables for Supabase
process.env.NEXT_PUBLIC_SUPABASE_URL = 'https://wzgxtvqkivbiinkoewmf.supabase.co';
process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY =
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind6Z3h0dnFraXZiaWlua29ld21mIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTc0NTM4MDEsImV4cCI6MjA3MzAyOTgwMX0.N4EcHLKB1EXyUVUTf3OhlJ6P-bss2C0A5xPvt7GQ3VE';
process.env.NEXT_PUBLIC_API_BASE_URL = 'http://127.0.0.1:8000';
