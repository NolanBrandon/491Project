// Use Next.js provided Jest preset to handle SWC/Babel transforms, ESM modules, CSS modules, etc.
const nextJest = require('next/jest');

const createJestConfig = nextJest({
  // Path to your Next.js app (root where next.config.* lives)
  dir: './'
});

/** @type {import('jest').Config} */
const customJestConfig = {
  testEnvironment: 'jest-environment-jsdom',
  // Setup scripts
  setupFilesAfterEnv: ['<rootDir>/jest.setup.ts'],
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json', 'node'],
  // Map path aliases & style imports
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
    '^.+\\.(css|less|scss|sass)$': 'identity-obj-proxy'
  },
  // Tell Jest to transform specific ESM packages inside node_modules that ship untranspiled code.
  // Anything not listed here remains ignored for performance.
  transformIgnorePatterns: [
    '/node_modules/(?!(framer-motion|@nextui-org|@heroui|@heroui/react|@heroui/navbar)/)'
  ],
  testMatch: [
    '<rootDir>/src/**/__tests__/**/*.(ts|tsx|js|jsx)',
    '<rootDir>/src/**/*.(test|spec).(ts|tsx|js|jsx)'
  ],
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/types.{ts,tsx}',
    '!src/**/*.d.ts'
  ]
};

module.exports = createJestConfig(customJestConfig);
