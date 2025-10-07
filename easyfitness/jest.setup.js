import '@testing-library/jest-dom';
import React from 'react';

jest.mock('next/link', () => {
  return ({ children, href }) => <a href={href}>{children}</a>;
});

jest.mock('next/navigation', () => ({
  useRouter: () => ({ push: jest.fn(), prefetch: jest.fn() }),
}));
