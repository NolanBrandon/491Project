Workout Plan Generator Page - Unit Test Documentation

1. Rendering Tests

File: easyfitness/src/app/__tests__/workout-plan-generator.test.tsx

Status: Created and Passing (5/31 tests)

Run Command: cd easyfitness && npm test -- workout-plan-generator.test.tsx

Areas Tested:
- renders workout plan generator heading (Component renders main heading)
- renders navbar (Navbar component is present)
- shows loading state for goals (Loading state displays while fetching goals)
- shows message when no active goal (Empty state message when no active goal)
- displays active goal when available (Goal information displays correctly)


2. Workout Plan Form Tests

File: easyfitness/src/app/__tests__/workout-plan-generator.test.tsx

Status: Created and Passing (7/31 tests)

Run Command: cd easyfitness && npm test -- workout-plan-generator.test.tsx

Areas Tested:
- renders experience level selector (Experience level dropdown with default value)
- renders days per week selector (Days per week dropdown with default value)
- renders save plan checkbox (Checkbox renders and is checked by default)
- renders generate workout plan button (Generate button is present)
- allows changing experience level (User can change experience level selection)
- allows changing days per week (User can change days per week selection)
- allows toggling save plan checkbox (Checkbox can be toggled)


3. Recent Workouts Feature Tests

File: easyfitness/src/app/__tests__/workout-plan-generator.test.tsx

Status: Created and Passing (9/31 tests)

Run Command: cd easyfitness && npm test -- workout-plan-generator.test.tsx

Areas Tested:
- renders add exercises from recent workouts button (Button to open modal is rendered)
- opens recent workouts modal when button is clicked (Modal opens on button click)
- closes modal when close is clicked (Modal closes when close button is clicked)
- displays selected exercises after adding from recent workouts (Exercises appear in selected section after adding)
- shows exercise count in selected exercises header (Header displays correct exercise count)
- allows removing individual exercises (Individual exercises can be removed from selection)
- allows clearing all selected exercises (All exercises can be cleared at once)
- passes existing exercise names to modal for duplicate detection (Duplicate prevention works correctly)
- hides selected exercises section when no exercises are selected (Section is hidden when empty)


4. Workout Plan Generation Tests

File: easyfitness/src/app/__tests__/workout-plan-generator.test.tsx

Status: Created and Passing (5/31 tests)

Run Command: cd easyfitness && npm test -- workout-plan-generator.test.tsx

Areas Tested:
- generates workout plan on form submit (Plan generation API is called with correct parameters)
- navigates to plan detail page after successful generation (Navigation to plan detail page)
- merges selected exercises into generated plan (Exercises from recent workouts are merged into plan)
- shows loading state during generation (Loading state displays during plan generation)
- displays error message on generation failure (Error handling when generation fails)


5. Saved Plans Display Tests

File: easyfitness/src/app/__tests__/workout-plan-generator.test.tsx

Status: Created and Passing (3/31 tests)

Run Command: cd easyfitness && npm test -- workout-plan-generator.test.tsx

Areas Tested:
- displays saved workout plans (Saved plans section renders with plan names and descriptions)
- shows loading state for saved plans (Loading state displays while fetching saved plans)
- shows message when no saved plans (Empty state message when user has no saved plans)


6. Authentication Tests

File: easyfitness/src/app/__tests__/workout-plan-generator.test.tsx

Status: Created and Passing (2/31 tests)

Run Command: cd easyfitness && npm test -- workout-plan-generator.test.tsx

Areas Tested:
- redirects to login when not authenticated (Unauthenticated users are redirected to login)
- does not redirect when authenticated (Authenticated users can access the page)

