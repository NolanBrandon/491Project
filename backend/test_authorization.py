#!/usr/bin/env python
"""
Test script for authorization and permissions
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000/api"

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def create_test_users():
    """Create two test users for authorization testing"""
    print_section("SETUP: Creating Test Users")
    
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    
    users = []
    for i in [1, 2]:
        user_data = {
            "username": f"authtest_user{i}_{timestamp}",
            "email": f"authtest{i}_{timestamp}@example.com",
            "password": "TestPass123!",
            "password_confirm": "TestPass123!",
            "gender": "other",
            "date_of_birth": "1995-05-15"
        }
        
        response = requests.post(f"{BASE_URL}/users/", json=user_data)
        
        if response.status_code == 201:
            data = response.json()
            cookie = response.cookies.get('easyfitness_session')
            users.append({
                'user_id': data['user']['id'],
                'username': data['user']['username'],
                'cookie': cookie
            })
            print(f"✅ Created User {i}: {data['user']['username']}")
        else:
            print(f"❌ Failed to create User {i}")
            print(response.json())
    
    return users

def test_unauthenticated_access():
    """Test that protected endpoints reject unauthenticated requests"""
    print_section("TEST 1: Unauthenticated Access Protection")
    
    endpoints = [
        ('GET', '/user-metrics/'),
        ('GET', '/goals/'),
        ('GET', '/workout-plans/'),
        ('GET', '/workout-logs/'),
        ('GET', '/nutrition-logs/'),
        ('GET', '/meal-plans/'),
    ]
    
    passed = 0
    for method, endpoint in endpoints:
        response = requests.request(method, f"{BASE_URL}{endpoint}")
        if response.status_code == 401:
            print(f"✅ {method} {endpoint} - Correctly rejected (401)")
            passed += 1
        else:
            print(f"❌ {method} {endpoint} - Should reject but got {response.status_code}")
    
    print(f"\n{passed}/{len(endpoints)} endpoints properly protected")

def test_user_data_isolation(users):
    """Test that users can only access their own data"""
    print_section("TEST 2: User Data Isolation")
    
    if len(users) < 2:
        print("⚠️  Need at least 2 users for isolation test")
        return
    
    user1, user2 = users[0], users[1]
    
    # User 1 creates a goal
    print(f"\nUser 1 ({user1['username']}) creating a goal...")
    goal_data = {
        "user": user1['user_id'],
        "goal_type": "weight_loss",
        "target_weight_kg": 70.0,
        "start_date": "2025-10-15",
        "end_date": "2026-01-15",
        "is_active": True
    }
    
    response = requests.post(
        f"{BASE_URL}/goals/",
        json=goal_data,
        cookies={'easyfitness_session': user1['cookie']}
    )
    
    if response.status_code == 201:
        goal_id = response.json()['id']
        print(f"✅ Goal created: {goal_id}")
        
        # User 1 should see their goal
        print(f"\nUser 1 retrieving their goals...")
        response = requests.get(
            f"{BASE_URL}/goals/",
            cookies={'easyfitness_session': user1['cookie']}
        )
        
        if response.status_code == 200:
            goals_data = response.json()
            # Handle paginated response
            goals = goals_data.get('results', goals_data) if isinstance(goals_data, dict) else goals_data
            if len(goals) > 0:
                print(f"✅ User 1 can see their own goals ({len(goals)} goals)")
            else:
                print("❌ User 1 should see their goals")
        
        # User 2 should NOT see User 1's goals
        print(f"\nUser 2 attempting to retrieve goals...")
        response = requests.get(
            f"{BASE_URL}/goals/",
            cookies={'easyfitness_session': user2['cookie']}
        )
        
        if response.status_code == 200:
            goals_data = response.json()
            # Handle paginated response
            goals = goals_data.get('results', goals_data) if isinstance(goals_data, dict) else goals_data
            if len(goals) == 0:
                print(f"✅ User 2 correctly sees no goals (data isolation working)")
            else:
                print(f"❌ User 2 should not see User 1's goals but saw {len(goals)} goals")
    else:
        print(f"❌ Failed to create goal: {response.status_code}")

def test_dashboard_access(users):
    """Test that users can only access their own dashboard"""
    print_section("TEST 3: Dashboard Access Control")
    
    if len(users) < 2:
        print("⚠️  Need at least 2 users for dashboard test")
        return
    
    user1, user2 = users[0], users[1]
    
    # User 1 accessing their own dashboard
    print(f"User 1 accessing their own dashboard...")
    response = requests.get(
        f"{BASE_URL}/users/{user1['user_id']}/dashboard/",
        cookies={'easyfitness_session': user1['cookie']}
    )
    
    if response.status_code == 200:
        print(f"✅ User 1 can access their own dashboard")
    else:
        print(f"❌ User 1 should access their own dashboard but got {response.status_code}")
    
    # User 2 trying to access User 1's dashboard
    print(f"\nUser 2 attempting to access User 1's dashboard...")
    response = requests.get(
        f"{BASE_URL}/users/{user1['user_id']}/dashboard/",
        cookies={'easyfitness_session': user2['cookie']}
    )
    
    if response.status_code == 403:
        print(f"✅ User 2 correctly denied access to User 1's dashboard (403)")
    else:
        print(f"❌ User 2 should be denied but got {response.status_code}")

def test_ai_generation_authorization(users):
    """Test that users can only generate plans for themselves"""
    print_section("TEST 4: AI Plan Generation Authorization")
    
    if len(users) < 2:
        print("⚠️  Need at least 2 users for AI generation test")
        return
    
    user1, user2 = users[0], users[1]
    
    # User 2 trying to generate workout plan for User 1
    print(f"User 2 attempting to generate workout plan for User 1...")
    workout_data = {
        "user_id": user1['user_id'],  # User 1's ID
        "user_goal": "build muscle",
        "experience_level": "beginner",
        "days_per_week": 3,
        "save_plan": False
    }
    
    response = requests.post(
        f"{BASE_URL}/generate-workout-plan/",
        json=workout_data,
        cookies={'easyfitness_session': user2['cookie']}  # User 2's session
    )
    
    if response.status_code == 403:
        print(f"✅ Correctly denied - User 2 cannot generate plan for User 1 (403)")
    else:
        print(f"❌ Should deny cross-user plan generation but got {response.status_code}")
        if response.status_code != 403:
            print(f"Response: {response.json()}")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("  🔒 AUTHORIZATION & PERMISSIONS TEST SUITE")
    print("="*60)
    
    try:
        # Setup
        users = create_test_users()
        
        if len(users) < 2:
            print("\n❌ ERROR: Failed to create test users. Cannot continue.")
            exit(1)
        
        # Run tests
        test_unauthenticated_access()
        test_user_data_isolation(users)
        test_dashboard_access(users)
        test_ai_generation_authorization(users)
        
        print("\n" + "="*60)
        print("  ✅ AUTHORIZATION TEST SUITE COMPLETE")
        print("="*60 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to server at http://localhost:8000")
        print("Make sure the Django server is running\n")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}\n")
        import traceback
        traceback.print_exc()
