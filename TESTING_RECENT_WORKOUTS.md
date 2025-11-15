# Testing Guide: Recent Workouts Quick Add Feature

This guide covers how to test the Recent Workouts Quick Add feature, including backend API tests, manual API testing, and frontend UI testing.

## Table of Contents
1. [Backend API Tests](#backend-api-tests)
2. [Manual API Testing](#manual-api-testing)
3. [Frontend UI Testing](#frontend-ui-testing)
4. [End-to-End Testing](#end-to-end-testing)

---

## Backend API Tests

### Run Automated Tests

```bash
cd backend
source easyfitness_env/bin/activate

# Run all recent workouts tests
python manage.py test tests.test_recent_workouts --verbosity=2

# Run with keepdb flag to reuse test database
python manage.py test tests.test_recent_workouts --verbosity=2 --keepdb

# Run specific test
python manage.py test tests.test_recent_workouts.RecentWorkoutsTestCase.test_get_recent_workouts_returns_grouped_sessions
```

### Test Coverage

The test suite covers:
- ✅ Authentication requirement
- ✅ Workout sessions grouped by date
- ✅ Limit parameter functionality
- ✅ Days parameter (excluding old workouts)
- ✅ Duplicate exercise removal within sessions
- ✅ Exercise details included in response
- ✅ User isolation (users only see their own workouts)
- ✅ Empty response handling

---

## Manual API Testing

### Prerequisites

1. **Start the backend server:**
```bash
cd backend
source easyfitness_env/bin/activate
python manage.py runserver
```

2. **Login to get session cookie:**
You need to be authenticated. First, login through the frontend or API to get a session cookie.

### Test Setup: Create Sample Workout Logs

Before testing the recent workouts endpoint, create some workout logs:

```bash
# Replace SESSION_COOKIE with your actual session cookie from login
# Replace USER_ID with your user UUID

# Create workout log for today
curl -X POST http://localhost:8000/api/workout-logs/ \
  -H "Content-Type: application/json" \
  -H "Cookie: easyfitness_session=YOUR_SESSION_COOKIE" \
  -d '{
    "exercise_name": "Push-ups",
    "sets_performed": 3,
    "reps_performed": 10,
    "perceived_effort": 7
  }'

# Create another workout log for today
curl -X POST http://localhost:8000/api/workout-logs/ \
  -H "Content-Type: application/json" \
  -H "Cookie: easyfitness_session=YOUR_SESSION_COOKIE" \
  -d '{
    "exercise_name": "Squats",
    "sets_performed": 3,
    "reps_performed": 12,
    "perceived_effort": 6
  }'

# Create workout log for yesterday (optional - you may need to manually set date_performed in database)
```

### Test the Recent Workouts Endpoint

```bash
# Basic request - get recent workouts
curl -X GET "http://localhost:8000/api/workout-logs/recent-workouts/" \
  -H "Cookie: easyfitness_session=YOUR_SESSION_COOKIE"

# With limit parameter
curl -X GET "http://localhost:8000/api/workout-logs/recent-workouts/?limit=5" \
  -H "Cookie: easyfitness_session=YOUR_SESSION_COOKIE"

# With days parameter
curl -X GET "http://localhost:8000/api/workout-logs/recent-workouts/?days=7" \
  -H "Cookie: easyfitness_session=YOUR_SESSION_COOKIE"

# With both parameters
curl -X GET "http://localhost:8000/api/workout-logs/recent-workouts/?limit=10&days=30" \
  -H "Cookie: easyfitness_session=YOUR_SESSION_COOKIE"

# Test without authentication (should return 401)
curl -X GET "http://localhost:8000/api/workout-logs/recent-workouts/"
```

### Expected Response Format

```json
{
  "success": true,
  "recent_workouts": [
    {
      "date": "2024-01-15",
      "timestamp": "2024-01-15T10:30:00Z",
      "exercise_count": 2,
      "total_exercises": 2,
      "exercises": [
        {
          "exercise_name": "Push-ups",
          "sets_performed": 3,
          "reps_performed": 10,
          "duration_minutes": null,
          "calories_burned": null,
          "perceived_effort": 7
        },
        {
          "exercise_name": "Squats",
          "sets_performed": 3,
          "reps_performed": 12,
          "duration_minutes": null,
          "calories_burned": null,
          "perceived_effort": 6
        }
      ]
    }
  ],
  "count": 1
}
```

### Testing with Django Shell

You can also create test data using Django shell:

```bash
cd backend
source easyfitness_env/bin/activate
python manage.py shell
```

```python
from api.models import User, WorkoutLog
from django.utils import timezone
from datetime import timedelta

# Get or create a test user
user = User.objects.first()  # Or get a specific user

# Create workout logs for different dates
now = timezone.now()

# Today's workout
WorkoutLog.objects.create(
    user=user,
    exercise_name="Push-ups",
    sets_performed=3,
    reps_performed=10,
    perceived_effort=7
)

WorkoutLog.objects.create(
    user=user,
    exercise_name="Squats",
    sets_performed=3,
    reps_performed=12,
    perceived_effort=6
)

# Yesterday's workout (you may need to manually set date_performed)
yesterday = now - timedelta(days=1)
log_yesterday = WorkoutLog.objects.create(
    user=user,
    exercise_name="Bench Press",
    sets_performed=4,
    reps_performed=8,
    perceived_effort=8
)
log_yesterday.date_performed = yesterday
log_yesterday.save()
```

---

## Frontend UI Testing

### Prerequisites

1. **Start the backend server:**
```bash
cd backend
source easyfitness_env/bin/activate
python manage.py runserver
```

2. **Start the frontend server:**
```bash
cd easyfitness
npm run dev
```

### Test Steps

1. **Login to the application**
   - Navigate to `http://localhost:3000/login`
   - Login with your credentials

2. **Create some workout logs** (to have recent workouts to select from)
   - You can create workout logs via the API (see Manual API Testing above)
   - Or use any existing feature in the app that creates workout logs

3. **Navigate to Workout Plan Generator**
   - Go to `http://localhost:3000/workout-plan-generator`
   - You should see the "Add Exercises from Recent Workouts" button

4. **Test the Recent Workouts Modal**
   - Click "Add Exercises from Recent Workouts" button
   - Modal should open showing recent workout sessions
   - Verify:
     - Recent workouts are displayed grouped by date
     - Each workout shows exercise count
     - Preview of first 3 exercises is shown

5. **Test Exercise Selection**
   - Click "Select" on a recent workout
   - Modal should show exercise selection view
   - Verify:
     - All exercises from that workout are listed
     - Each exercise shows sets and reps
     - Checkboxes allow selection
     - "Add Selected Exercises" button shows count

6. **Test Duplicate Detection**
   - Select some exercises and click "Add Selected Exercises"
   - Exercises should appear in the green box above the form
   - Click "Add Exercises from Recent Workouts" again
   - Select the same workout
   - Verify:
     - Previously added exercises show "Already Added" badge
     - Checkboxes for duplicates are disabled
     - Only non-duplicate exercises can be selected

7. **Test Adding Exercises**
   - Select new exercises (not duplicates)
   - Click "Add Selected Exercises"
   - Verify:
     - Exercises are added to the selected exercises list
     - List shows exercise name, sets, and reps
     - Each exercise has a "Remove" button

8. **Test Removing Exercises**
   - Click "Remove" on an exercise in the selected list
   - Verify exercise is removed from the list

9. **Test Workout Plan Generation with Selected Exercises**
   - Ensure you have selected exercises from recent workouts
   - Fill in the workout plan form (Experience Level, Days Per Week)
   - Click "Generate Workout Plan"
   - Verify:
     - Plan is generated successfully
     - Selected exercises are included in the generated plan
     - Navigate to the workout plan detail page and verify exercises are present

### Expected UI Behavior

- **Modal should:**
  - Open smoothly when button is clicked
  - Close when clicking outside, X button, or after adding exercises
  - Show loading state while fetching workouts
  - Show error message if API call fails
  - Show empty state if no recent workouts exist

- **Exercise selection should:**
  - Pre-select all non-duplicate exercises when a workout is selected
  - Allow toggling individual exercise selection
  - Disable duplicate exercises
  - Show count of selected exercises on the "Add" button

- **Selected exercises display should:**
  - Show in a green highlighted box
  - Display exercise name, sets, and reps
  - Allow removing individual exercises
  - Allow clearing all exercises

---

## End-to-End Testing

### Complete User Flow Test

1. **Setup: Create workout logs**
   ```bash
   # Use API or Django shell to create multiple workout logs
   # with different dates to have recent workout history
   ```

2. **User Action Flow:**
   - Login to application
   - Navigate to Workout Plan Generator
   - Click "Add Exercises from Recent Workouts"
   - Browse recent workouts
   - Select a workout session
   - Select specific exercises to add
   - Add exercises (should appear in green box)
   - Add more exercises from a different workout
   - Verify duplicates are prevented
   - Fill in workout plan form
   - Generate workout plan
   - Verify generated plan includes selected exercises

3. **Edge Cases to Test:**
   - No recent workouts (should show empty state)
   - All exercises are duplicates (should show message)
   - Network error (should show error message with retry)
   - Invalid session (should redirect to login)

---

## Troubleshooting

### Backend Issues

**Problem:** Tests fail with database error
```bash
# Solution: Use --keepdb flag or drop test database
python manage.py test tests.test_recent_workouts --keepdb
```

**Problem:** 401 Unauthorized error
- Check that session cookie is being sent
- Verify user is logged in
- Check session middleware is configured

**Problem:** No workouts returned
- Verify workout logs exist for the authenticated user
- Check date range (default is 30 days)
- Verify workout logs have `date_performed` within range

### Frontend Issues

**Problem:** Modal doesn't open
- Check browser console for errors
- Verify RecentWorkoutsModal component is imported
- Check that `showRecentWorkoutsModal` state is being set

**Problem:** No workouts displayed
- Check browser console for API errors
- Verify API endpoint is accessible
- Check network tab for failed requests
- Verify workout logs exist in database

**Problem:** Exercises not added to plan
- Check browser console for errors
- Verify selected exercises are in state
- Check plan generation logic merges exercises correctly

---

## API Endpoint Reference

**Endpoint:** `GET /api/workout-logs/recent-workouts/`

**Query Parameters:**
- `limit` (optional, default: 10): Maximum number of workout sessions to return
- `days` (optional, default: 30): Number of days to look back

**Authentication:** Required (session-based)

**Response:**
```json
{
  "success": true,
  "recent_workouts": [...],
  "count": 1
}
```

---

## Quick Test Checklist

- [ ] Backend tests pass
- [ ] API endpoint returns 401 without authentication
- [ ] API endpoint returns workouts for authenticated user
- [ ] Workouts are grouped by date
- [ ] Duplicates are removed within sessions
- [ ] Limit parameter works
- [ ] Days parameter works
- [ ] Frontend modal opens and closes correctly
- [ ] Recent workouts are displayed
- [ ] Exercise selection works
- [ ] Duplicate detection works in UI
- [ ] Exercises can be added to plan
- [ ] Exercises are merged into generated plan
- [ ] Error states are handled gracefully
- [ ] Empty states are handled gracefully

