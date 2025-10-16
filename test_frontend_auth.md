# Frontend Authentication Testing - Phase 4

## Test Setup
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Both servers are running ✅

## IMPORTANT: API Endpoints
The auth endpoints are accessed via the UserViewSet router:
- Registration: POST /api/users/
- Login: POST /api/users/login/
- Logout: POST /api/users/logout/
- Session: GET /api/users/session/
- Validate: GET /api/users/validate_session/

## Test User Created
- Username: testfrontenduser
- Email: testfrontend@test.com
- Password: TestPass123!

## Manual Test Cases

### Test 1: User Registration Flow
1. Navigate to http://localhost:3000/signup
2. Fill out the registration form:
   - Username: newfrontenduser
   - Email: newfrontend@example.com
   - Password: TestPass123!
   - Confirm Password: TestPass123!
   - Gender: male
   - Date of Birth: 1990-01-01
3. Click "Sign Up"
4. Expected: Auto-login, redirect to /mylog, see username in navbar

### Test 2: User Login Flow
1. Navigate to http://localhost:3000/login
2. Enter credentials:
   - Username or Email: testfrontenduser
   - Password: TestPass123!
3. Click "Login"
4. Expected: Successful login, redirect to /mylog, see username in navbar

### Test 3: Session Persistence
1. After logging in (Test 2)
2. Refresh the page (F5 or Cmd+R)
3. Expected: User stays logged in, still see username in navbar

### Test 4: Logout Flow
1. While logged in
2. Click the "Logout" button in navbar
3. Expected: Redirect to /login, no longer authenticated

### Test 5: Protected Route Access
1. While logged out
2. Try to navigate to http://localhost:3000/mylog
3. Expected: Should see the page (or implement redirect if needed)

## Browser Console Checks
- Check Network tab for:
  - POST /api/users/login/ (should set Set-Cookie header)
  - GET /api/users/session/ (should include Cookie header)
  - Cookie should be HttpOnly, SameSite=Lax
  
## Expected Issues to Note
- We haven't implemented route protection yet (Phase 5)
- Auto-session validation on page load not implemented yet (Phase 5)
- Error handling could be improved

## Test Results
(To be filled after manual testing)
