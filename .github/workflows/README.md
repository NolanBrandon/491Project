# CI/CD Workflows

This directory contains GitHub Actions workflows for the EasyFitness project.

## Frontend Build & Test Workflow

**File:** `frontend-build.yml`

**Triggers:**
- Pull requests that modify frontend code (`easyfitness/**`)
- Pushes to `main` or `develop` branches

**Jobs:**

### 1. Frontend Tests (`test`)
- **Matrix:** Node.js 18.x and 20.x
- **Steps:**
  - Checkout code
  - Setup Node.js with caching
  - Install dependencies
  - Type checking with TypeScript
  - Linting with ESLint
  - Unit tests with Jest
  - Build verification
  - Upload test results and build artifacts

### 2. Code Coverage (`coverage`)
- **Runtime:** Node.js 20.x
- **Steps:**
  - Run tests with coverage collection
  - Generate coverage reports (HTML, LCOV, JSON)
  - Upload coverage artifacts
  - Comment coverage summary on PRs

### 3. Dependency Security Check (`dependency-check`)
- **Runtime:** Node.js 20.x
- **Steps:**
  - Security audit with `npm audit`
  - Check for outdated dependencies
  - Validate package-lock.json integrity

### 4. Deployment Readiness (`deployment-readiness`)
- **Runtime:** Node.js 20.x
- **Conditions:** Only on pull requests, after test and coverage jobs
- **Steps:**
  - Production build test
  - Server startup verification
  - Bundle size analysis
  - Basic Lighthouse performance check

### 5. Status Check (`status-check`)
- **Purpose:** Aggregate status of all jobs
- **Conditions:** Always runs, depends on all other jobs
- **Steps:**
  - Check individual job results
  - Provide consolidated pass/fail status

## Test Coverage

The workflow enforces minimum coverage thresholds:
- **Branches:** 50%
- **Functions:** 50%
- **Lines:** 50%
- **Statements:** 50%

## Artifacts

The following artifacts are generated and stored:
- **Test Results:** JUnit XML format for test reporting
- **Coverage Reports:** HTML and LCOV format
- **Build Artifacts:** Next.js build output (excluding cache)

## Badge Status

Add this badge to your README to show build status:

```markdown
![Frontend Build](https://github.com/BXM22/491Project/actions/workflows/frontend-build.yml/badge.svg)
```

## Local Development

To run the same checks locally:

```bash
cd easyfitness

# Type checking
npx tsc --noEmit

# Linting
npm run lint

# Tests
npm test

# Tests with coverage
npm test -- --coverage

# Production build
npm run build

# Security audit
npm audit
```

## Troubleshooting

### Common Issues

1. **Type errors:** Run `npx tsc --noEmit` locally to see type issues
2. **Lint errors:** Run `npm run lint` and fix reported issues
3. **Test failures:** Run `npm test` locally and check test output
4. **Build failures:** Ensure all dependencies are properly installed
5. **Coverage below threshold:** Add more test cases or adjust thresholds

### Configuration Files

- **Jest:** `jest.config.js` - Test configuration and coverage settings
- **TypeScript:** `tsconfig.json` - TypeScript compiler options
- **ESLint:** `eslint.config.mjs` - Linting rules and configuration