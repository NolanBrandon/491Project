#!/usr/bin/env python
"""
Test script for session-based authentication endpoints
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000/api"

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_user_creation_and_session():
    """Test user creation with auto-login"""
    print_section("TEST 1: User Creation with Auto-Login")
    
    # Create a test user with unique timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    user_data = {
        "username": f"testuser_{timestamp}",
        "email": f"test_{timestamp}@example.com",
        "password": "TestPass123!",
        "password_confirm": "TestPass123!",
        "gender": "other",
        "date_of_birth": "1995-05-15"
    }
    
    print("Creating new user...")
    response = requests.post(
        f"{BASE_URL}/users/",
        json=user_data
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Check if session cookie was set
    if 'easyfitness_session' in response.cookies:
        print("✅ Session cookie set on registration!")
        session_cookie = response.cookies['easyfitness_session']
        return session_cookie
    else:
        print("❌ No session cookie found")
        print(f"Cookies: {response.cookies}")
        return None

def test_session_validation(session_cookie):
    """Test session validation endpoint"""
    print_section("TEST 2: Session Validation")
    
    if not session_cookie:
        print("⚠️  No session cookie to test with")
        return
    
    cookies = {'easyfitness_session': session_cookie}
    
    print("Validating session...")
    response = requests.get(
        f"{BASE_URL}/users/validate_session/",  # underscore not hyphen
        cookies=cookies
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print("✅ Session is valid!")
    else:
        print("❌ Session validation failed")

def test_get_session_user(session_cookie):
    """Test getting current session user"""
    print_section("TEST 3: Get Session User")
    
    if not session_cookie:
        print("⚠️  No session cookie to test with")
        return
    
    cookies = {'easyfitness_session': session_cookie}
    
    print("Getting current user from session...")
    response = requests.get(
        f"{BASE_URL}/users/session/",
        cookies=cookies
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print("✅ Successfully retrieved session user!")
    else:
        print("❌ Failed to get session user")

def test_login():
    """Test login endpoint"""
    print_section("TEST 4: Login Endpoint")
    
    login_data = {
        "username": "testuser_session",  # Use existing user from first run
        "password": "TestPass123!"
    }
    
    print("Logging in...")
    response = requests.post(
        f"{BASE_URL}/users/login/",
        json=login_data
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if 'easyfitness_session' in response.cookies:
        print("✅ Session cookie set on login!")
        return response.cookies['easyfitness_session']
    else:
        print("❌ No session cookie found")
        return None

def test_logout(session_cookie):
    """Test logout endpoint"""
    print_section("TEST 5: Logout Endpoint")
    
    if not session_cookie:
        print("⚠️  No session cookie to test with")
        return
    
    cookies = {'easyfitness_session': session_cookie}
    
    print("Logging out...")
    response = requests.post(
        f"{BASE_URL}/users/logout/",
        cookies=cookies
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print("✅ Successfully logged out!")
    else:
        print("❌ Logout failed")
    
    # Verify session is invalid after logout
    print("\nVerifying session is invalid after logout...")
    validate_response = requests.get(
        f"{BASE_URL}/users/validate_session/",  # underscore not hyphen
        cookies=cookies
    )
    
    if validate_response.status_code == 401:
        print("✅ Session correctly invalidated after logout!")
    else:
        print("❌ Session still valid after logout")

def test_unauthenticated_access():
    """Test accessing protected endpoint without session"""
    print_section("TEST 6: Unauthenticated Access")
    
    print("Attempting to access session endpoint without cookie...")
    response = requests.get(f"{BASE_URL}/users/session/")
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 401:
        print("✅ Correctly rejected unauthenticated request!")
    else:
        print("❌ Should have rejected unauthenticated request")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("  🔐 SESSION AUTHENTICATION TEST SUITE")
    print("="*60)
    
    try:
        # Run tests
        session_cookie = test_user_creation_and_session()
        test_session_validation(session_cookie)
        test_get_session_user(session_cookie)
        test_logout(session_cookie)
        
        # Test login separately
        login_cookie = test_login()
        test_logout(login_cookie)
        
        # Test unauthenticated access
        test_unauthenticated_access()
        
        print("\n" + "="*60)
        print("  ✅ TEST SUITE COMPLETE")
        print("="*60 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to server at http://localhost:8000")
        print("Make sure the Django server is running with: python manage.py runserver\n")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}\n")
