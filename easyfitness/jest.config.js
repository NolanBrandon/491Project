/* eslint-disable @typescript-eslint/no-require-imports */
// Use Next.js provided Jest preset to handle SWC/Babel transforms, ESM modules, CSS modules, etc.
const nextJest = require('next/jest');

const createJestConfig = nextJest({
  dir: './', // Path to your Next.js app
});


/** @type {import('jest').Config} */
const customJestConfig = {
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/jest.setup.ts'],
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
  },
  transform: {
    '^.+\\.(js|jsx|ts|tsx)$': 'babel-jest',
  },
  transformIgnorePatterns: [
    '/node_modules/(?!(axios|@supabase|@heroui|@nextui-org)/)',
  ],
  testMatch: [
    '<rootDir>/src/**/__tests__/**/*.{ts,tsx,js,jsx}',
    '<rootDir>/src/**/*.{test,spec}.{ts,tsx,js,jsx}'
  ],
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/types.{ts,tsx}',
    '!src/**/*.d.ts'
  ],
  // Coverage thresholds for CI/CD
  coverageThreshold: {
    global: {
      branches: 50,
      functions: 50,
      lines: 50,
      statements: 50
    }
  },
  // Coverage reporting
  coverageReporters: ['text', 'lcov', 'html', 'json-summary'],
  // Test timeout for CI environments
  testTimeout: 10000,
  // Fail fast in CI
  bail: process.env.CI ? 1 : 0,
  // Always show individual test results
  verbose: true
};

// Export the Jest config
module.exports = createJestConfig(customJestConfig);
