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
// jest.setup.ts
process.env.NEXT_PUBLIC_SUPABASE_URL ||= 'https://mock.supabase.co';
process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY ||= 'mock-anon-key-for-testing-only';

process.env.NEXT_PUBLIC_API_BASE_URL = 'http://127.0.0.1:8000';
