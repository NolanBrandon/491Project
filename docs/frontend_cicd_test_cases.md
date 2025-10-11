# Frontend CI/CD Test Cases

This document summarizes the automated frontend CI/CD checks for the EasyFitness project in a clear, test-case oriented format.

---

Test Case 1.1: Frontend Unit Tests (Jest CI)
Test Command: npm run test:ci
Purpose: Run React unit tests and produce JUnit reports for CI
Execution: GitHub Actions job “Frontend Tests” → step “Run Unit Tests”; local: `cd easyfitness && npm run test:ci`
Test Sequence:
1.1.1: Install Dependencies
Purpose: Ensure a clean, reproducible environment (npm ci)
Expected Output:
- Success: "added X packages" and exit code 0
- Failure: "ERR! ..." and non-zero exit code

1.1.2: Execute Jest in CI Mode
Purpose: Run tests and generate JUnit XML
Expected Output:
- Success: "Tests: … passed" and `easyfitness/test-results/junit.xml` exists
- Failure: "Tests: … failed" and non-zero exit code

---

Test Case 1.2: TypeScript Type Check
Test Command: npx tsc --noEmit
Purpose: Verify type safety across the Next.js app
Execution: GitHub Actions job “Frontend Tests” → step “Type Check”; local: `cd easyfitness && npx tsc --noEmit`
Expected Output:
- Success: No output and exit code 0
- Failure: Type errors listed with file:line references

---

Test Case 1.3: ESLint Linting
Test Command: npm run lint
Purpose: Enforce code quality and style consistency
Execution: GitHub Actions job “Frontend Tests” → step “Run ESLint”; local: `cd easyfitness && npm run lint`
Expected Output:
- Success: No lint errors reported; exit code 0
- Failure: Errors listed; non-zero exit code

---

Test Case 1.4: Production Build Verification
Test Command: npm run build
Purpose: Ensure the Next.js app builds successfully in CI
Execution: GitHub Actions job “Frontend Tests” → step “Build Application”; local: `cd easyfitness && npm run build`
Test Sequence:
1.4.1: Check .next directory exists
1.4.2: Check .next/BUILD_ID exists
Expected Output:
- Success: "Build verification successful"
- Failure: "Build failed: .next directory not found" or "BUILD_ID not found"

---
Test Case 1.5: Dependency Security Audit
Test Command: npm audit --audit-level=moderate
Purpose: Detect known vulnerabilities in dependencies
Execution: GitHub Actions job “Dependency Security Check”; local: `cd easyfitness && npm audit --audit-level=moderate`
Expected Output:
- Success: "found 0 vulnerabilities"
- Failure: Vulnerabilities reported; non-zero exit (fails the job)

---

Test Case 1.6: Deployment Readiness — Server Startup
Test Command: npm run start (after build), curl http://localhost:3000
Purpose: Validate that the production server can start and respond
Execution: GitHub Actions job “Deployment Readiness Check”; local: build then start and curl
Expected Output:
- Success: `curl -f` succeeds (HTTP 200); server started and then terminated
- Failure: "Server failed to start" or curl failure; non-zero exit code

---

Test Case 1.7: Bundle Size Report
Test Function: CI step scans `.next/static` for JS bundles
Purpose: Provide visibility into bundle size changes
Execution: GitHub Actions job “Deployment Readiness Check” → step “Check Bundle Size”
Expected Output:
- Success: A table appended to GitHub Step Summary with file sizes
- Failure: Missing `.next/static` or fs errors; step logs error

---

Test Case 1.8: Lighthouse CI (Basic)
Test Command: lhci autorun --upload.target=temporary-public-storage --collect.url=http://localhost:3000
Purpose: Basic performance and best-practices check on the built app
Execution: GitHub Actions job “Deployment Readiness Check” → step “Lighthouse CI (Basic)”
Expected Output:
- Success: Lighthouse results generated and uploaded; step is tolerant (won’t fail build)
- Failure: LHCI errors logged; step continues (non-blocking)

---

Test Case 1.9: Aggregated Status Gate
Test Function: Workflow job “All Checks Complete”
Purpose: Enforce that tests and security checks all passed
Execution: GitHub Actions job “Status Check” with `needs: [test, dependency-check]`
Expected Output:
- Success: "All checks passed! ✅"
- Failure: Emits specific failure message (e.g., "Tests failed", "Dependency check failed") and exits non-zero

---

Locations & Config
- Workflow: `.github/workflows/frontend-build.yml`
- Tests: `easyfitness/src/app/__tests__/*.test.tsx`
- Artifacts:
  - Test Results: `easyfitness/test-results/`
  - Build: `easyfitness/.next/` (cache excluded)