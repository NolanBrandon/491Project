import '@testing-library/jest-dom';
import React from 'react';

jest.mock('next/link', () => {
  const MockNextLink = ({ children, href }) => React.createElement('a', { href }, children);
  MockNextLink.displayName = 'MockNextLink';
  return MockNextLink;
});

jest.mock('next/navigation', () => ({
  useRouter: () => ({ push: jest.fn(), prefetch: jest.fn() }),
}));
