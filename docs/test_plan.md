# Sprint 2 Test Plan

## 1. Introduction & Purpose
This document describes the test strategy for the **491Project (EasyFitness)** application, a Django backend integrated with Supabase. The goal is to verify that backend APIs, database connections, and user-facing functionality (authentication, workout logging, etc.) are working correctly, reliable, and stable through automated tests.

The testing strategy also supports Continuous Integration / Continuous Deployment (CICD) to ensure that all new code changes are validated automatically before merging.

---

## 2. Testing Methodologies

We will apply the following methodologies:

- **Unit Testing**
  - Test Django models, serializers, and utility functions in isolation.
  - Example: verify that a `UserProfile` model calculates BMI correctly.
  
- **Integration Testing**
  - Test Django API endpoints against Supabase (using a test schema or mock data).
  - Example: POST `/api/login/` with valid/invalid credentials and confirm correct responses.
  
- **System Testing**
  - Validate complete user flows (end-to-end), such as:
    - Sign up → log in → add a workout → fetch workout history.
  
- **Regression Testing**
  - Ensure previously fixed bugs do not reappear.
  - Example: re-run tests for login/logout after authentication updates.
  
- **CICD-Driven Automated Testing**
  - All tests are executed in GitHub Actions pipelines whenever a PR is opened or code is pushed to `main`.

---

## 3. Scope

### In-Scope
- Django backend APIs (`/api/...` routes).
- Supabase database connection and queries.
- Authentication and user management.
- Automated test execution in CICD.

### Out-of-Scope (Sprint 2)
- Performance / load testing.
- UI/Frontend manual testing (covered by frontend team).
- Production deployment validation (planned for later sprints).

---

## 4. Test Environment & Tools
- **Languages/Frameworks:** Python, Django REST Framework
- **Testing Libraries:** `pytest`, `unittest`, Django’s built-in `TestCase`
- **Database:** Supabase (PostgreSQL)
- **CI/CD Platform:** GitHub Actions
- **Test Runner Command:**  
  ```bash
  python manage.py test

## 5. Responsibilities

Backend :

**Write and maintain unit + integration tests in backend/api/tests.py and backend/api/tests/.**

**Ensure test coverage for major features.**

**Document results in docs/test_results.md.**

Frontend  :

**Separate CI/CD pipeline for frontend.**

Will add UI tests later.

Shared:

**Review PRs for test quality.**

**Track bugs in GitHub Issues and docs/bugs.md.**


##  6. Schedule

Week 1: Create test plan, set up test cases for models and views.

Week 2: Expand integration tests (API endpoints, Supabase connection).

Week 3: Execute all tests via CI/CD, collect results, and document them.

## 7. Deliverables

Test Plan: docs/test_plan.md (this file).

Test Cases: backend/api/tests/ and backend/api/tests.py.

Test Results: docs/test_results.md.

Bug Tracking: docs/bugs.md linked to GitHub Issues.

## 8. Example Test Cases
Test ID	Description	Steps	Expected Result	Type
TC-001	User registration	POST /api/register/ with valid user data	201 Created + user returned	Integration
TC-002	Duplicate registration	POST /api/register/ with same email	400 Bad Request	Integration
TC-003	Login success	POST /api/login/ with valid credentials	200 OK + token returned	Integration
TC-004	Login failure	POST /api/login/ with wrong password	401 Unauthorized	Integration
TC-005	Add workout	POST /api/workouts/ with valid data	201 Created + workout saved	Integration
TC-006	Fetch workouts	GET /api/workouts/ after adding data	List contains created workout	System
TC-007	BMI calculation	Create UserProfile with height & weight	BMI computed correctly	Unit
TC-008	Migration check	Run python manage.py makemigrations	No missing migrations	Regression