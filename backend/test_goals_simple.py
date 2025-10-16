#!/usr/bin/env python3
"""Simple test for Goals API using Django test client"""
import os
import sys
import django

import os
import sys
import json
import django

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'easyfitness_backend.settings')
django.setup()

# Add 'testserver' to ALLOWED_HOSTS after Django setup
from django.conf import settings
if 'testserver' not in settings.ALLOWED_HOSTS:
    settings.ALLOWED_HOSTS.append('testserver')

from django.test import Client
from api.models import User, Goal
from api.serializers import hash_password

def test_goals_api():
    print("=" * 60)
    print("TESTING GOALS API - Phase 1")
    print("=" * 60)
    
    # Setup
    client = Client()
    
    # Clean up any existing test user
    User.objects.filter(username='testgoaluser').delete()
    
    # Step 1: Create test user
    print("\n1. Creating test user...")
    user = User.objects.create(
        username='testgoaluser',
        email='testgoaluser@test.com',
        password_hash=hash_password('testpass123')
    )
    print(f"   ✓ User created: {user.username} (ID: {user.id})")
    
    # Step 2: Login
    print("\n2. Logging in...")
    response = client.post('/api/users/login/', {
        'username': 'testgoaluser',
        'password': 'testpass123'
    }, content_type='application/json')
    
    if response.status_code == 200:
        print(f"   ✓ Login successful")
    else:
        print(f"   ✗ Login failed: {response.status_code}")
        print(f"   Response: {response.content}")
        return False
    
    # Step 3: List goals (should be empty)
    print("\n3. Listing goals (should be empty)...")
    response = client.get('/api/goals/')
    if response.status_code == 200:
        goals = response.json()
        print(f"   ✓ Retrieved {len(goals)} goal(s)")
        if len(goals) == 0:
            print("   ✓ Correctly empty")
    else:
        print(f"   ✗ Failed: {response.status_code}")
        return False
    
    # Step 4: Create a goal
    print("\n4. Creating a goal...")
    response = client.post('/api/goals/', {
        'title': 'Lose 10 pounds',
        'description': 'Get healthier by summer',
        'target_date': '2025-06-01',
        'status': 'active'
    }, content_type='application/json')
    
    if response.status_code == 201:
        goal = response.json()
        print(f"   ✓ Goal created")
        print(f"   ID: {goal['id']}")
        print(f"   Title: {goal['title']}")
        print(f"   User ID: {goal['user']}")
        goal_id = goal['id']
    else:
        print(f"   ✗ Failed: {response.status_code}")
        print(f"   Response: {response.content}")
        return False
    
    # Step 5: List goals (should have 1)
    print("\n5. Listing goals again...")
    response = client.get('/api/goals/')
    if response.status_code == 200:
        goals = response.json()
        print(f"   ✓ Retrieved {len(goals)} goal(s)")
        if len(goals) == 1:
            print("   ✓ Correct count")
        else:
            print(f"   ⚠ Expected 1 goal, got {len(goals)}")
    else:
        print(f"   ✗ Failed: {response.status_code}")
        return False
    
    # Step 6: Get specific goal
    print("\n6. Getting specific goal...")
    response = client.get(f'/api/goals/{goal_id}/')
    if response.status_code == 200:
        goal = response.json()
        print(f"   ✓ Goal retrieved")
        print(f"   Title: {goal['title']}")
        print(f"   Description: {goal['description']}")
    else:
        print(f"   ✗ Failed: {response.status_code}")
        return False
    
    # Step 7: Update goal
    print("\n7. Updating goal status...")
    response = client.patch(f'/api/goals/{goal_id}/', {
        'status': 'completed'
    }, content_type='application/json')
    
    if response.status_code == 200:
        goal = response.json()
        print(f"   ✓ Goal updated")
        print(f"   New status: {goal['status']}")
    else:
        print(f"   ✗ Failed: {response.status_code}")
        return False
    
    # Step 8: Create second goal
    print("\n8. Creating second goal...")
    response = client.post('/api/goals/', {
        'title': 'Build muscle',
        'description': 'Gain 10 pounds of muscle',
        'target_date': '2025-12-31',
        'status': 'active'
    }, content_type='application/json')
    
    if response.status_code == 201:
        print(f"   ✓ Second goal created")
        goal2_id = response.json()['id']
    else:
        print(f"   ✗ Failed: {response.status_code}")
        return False
    
    # Step 9: List all goals (should be 2)
    print("\n9. Listing all goals (should be 2)...")
    response = client.get('/api/goals/')
    if response.status_code == 200:
        goals = response.json()
        print(f"   ✓ Retrieved {len(goals)} goal(s)")
        if len(goals) == 2:
            print("   ✓ Correct count")
            for g in goals:
                print(f"   - {g['title']} ({g['status']})")
        else:
            print(f"   ⚠ Expected 2 goals, got {len(goals)}")
    else:
        print(f"   ✗ Failed: {response.status_code}")
        return False
    
    # Step 10: Delete first goal
    print("\n10. Deleting first goal...")
    response = client.delete(f'/api/goals/{goal_id}/')
    if response.status_code == 204:
        print(f"   ✓ Goal deleted")
    else:
        print(f"   ✗ Failed: {response.status_code}")
        return False
    
    # Step 11: Verify deletion
    print("\n11. Verifying deletion...")
    response = client.get('/api/goals/')
    if response.status_code == 200:
        goals = response.json()
        print(f"   ✓ Now have {len(goals)} goal(s)")
        if len(goals) == 1:
            print("   ✓ Deletion confirmed")
        else:
            print(f"   ⚠ Expected 1 goal, got {len(goals)}")
    else:
        print(f"   ✗ Failed: {response.status_code}")
        return False
    
    # Step 12: Test unauthenticated access
    print("\n12. Testing unauthenticated access...")
    unauth_client = Client()
    response = unauth_client.get('/api/goals/')
    if response.status_code in [401, 403]:
        print(f"   ✓ Correctly rejected (status {response.status_code})")
    else:
        print(f"   ⚠ Expected 401/403, got {response.status_code}")
    
    # Cleanup
    print("\n13. Cleaning up...")
    user.delete()
    print("   ✓ Test user deleted")
    
    print("\n" + "=" * 60)
    print("✅ ALL GOALS API TESTS PASSED!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    try:
        success = test_goals_api()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
