import '@testing-library/jest-dom';
import React from 'react';

jest.mock('next/link', () => {
  return ({ children, href }) => React.createElement('a', { href }, children);
});

jest.mock('next/navigation', () => ({
  useRouter: () => ({ push: jest.fn(), prefetch: jest.fn() }),
}));
