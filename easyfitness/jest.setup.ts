import '@testing-library/jest-dom';
import * as React from 'react';

// Minimal mock for next/link without using JSX in a .ts file
jest.mock('next/link', () => ({
  __esModule: true,
  default: (props: { children: React.ReactNode; href: string }) =>
    React.createElement('a', { href: props.href }, props.children),
}));

jest.mock('next/navigation', () => ({
  useRouter: () => ({ push: jest.fn(), prefetch: jest.fn() }),
}));
