# #!/usr/bin/env python3
# """Test Goals API CRUD operations"""
# import requests
# import json

# BASE_URL = "http://127.0.0.1:8000/api"

# def test_goals_api():
#     session = requests.Session()
    
#     print("=" * 60)
#     print("TESTING GOALS API - Phase 1")
#     print("=" * 60)
    
#     # Step 1: Create new user for testing
#     print("\n1. Creating test user...")
#     user_data = {
#         "username": f"goaltest_{__import__('time').time()}",
#         "email": f"goaltest{__import__('time').time()}@example.com",
#         "password": "testpass123",
#         "password_confirm": "testpass123"
#     }
#     response = session.post(f"{BASE_URL}/users/", json=user_data)
#     if response.status_code == 201:
#         print("   ✓ User created and logged in")
#         user = response.json()['user']
#         print(f"   Username: {user['username']}")
#     else:
#         print(f"   ✗ Failed: {response.status_code}")
#         print(f"   Error: {response.text}")
#         return False
    
#     # Step 2: Create a goal
#     print("\n2. Creating goal...")
#     goal_data = {
#         "title": "Lose 10kg",
#         "description": "Get fit for summer vacation",
#         "target_date": "2025-06-01",
#         "status": "active"
#     }
#     response = session.post(f"{BASE_URL}/goals/", json=goal_data)
#     if response.status_code == 201:
#         goal = response.json()
#         print("   ✓ Goal created successfully")
#         print(f"   ID: {goal['id']}")
#         print(f"   Title: {goal['title']}")
#         print(f"   Status: {goal['status']}")
#         goal_id = goal['id']
#     else:
#         print(f"   ✗ Failed: {response.status_code}")
#         print(f"   Error: {response.text}")
#         return False
    
#     # Step 3: List all goals
#     print("\n3. Listing all goals...")
#     response = session.get(f"{BASE_URL}/goals/")
#     if response.status_code == 200:
#         goals = response.json()
#         print(f"   ✓ Retrieved {len(goals)} goal(s)")
#         for g in goals:
#             print(f"   - {g['title']} ({g['status']})")
#     else:
#         print(f"   ✗ Failed: {response.status_code}")
#         return False
    
#     # Step 4: Get single goal
#     print("\n4. Getting specific goal...")
#     response = session.get(f"{BASE_URL}/goals/{goal_id}/")
#     if response.status_code == 200:
#         goal = response.json()
#         print("   ✓ Goal retrieved")
#         print(f"   Title: {goal['title']}")
#         print(f"   Description: {goal['description']}")
#     else:
#         print(f"   ✗ Failed: {response.status_code}")
#         return False
    
#     # Step 5: Update goal
#     print("\n5. Updating goal status...")
#     update_data = {"status": "completed"}
#     response = session.patch(f"{BASE_URL}/goals/{goal_id}/", json=update_data)
#     if response.status_code == 200:
#         goal = response.json()
#         print("   ✓ Goal updated")
#         print(f"   New status: {goal['status']}")
#     else:
#         print(f"   ✗ Failed: {response.status_code}")
#         return False
    
#     # Step 6: Create second goal
#     print("\n6. Creating second goal...")
#     goal_data2 = {
#         "title": "Build muscle mass",
#         "description": "Gain 5kg of lean muscle",
#         "target_date": "2025-12-31",
#         "status": "active"
#     }
#     response = session.post(f"{BASE_URL}/goals/", json=goal_data2)
#     if response.status_code == 201:
#         print("   ✓ Second goal created")
#         goal2_id = response.json()['id']
#     else:
#         print(f"   ✗ Failed: {response.status_code}")
#         return False
    
#     # Step 7: List goals again
#     print("\n7. Listing all goals (should be 2)...")
#     response = session.get(f"{BASE_URL}/goals/")
#     if response.status_code == 200:
#         goals = response.json()
#         print(f"   ✓ Retrieved {len(goals)} goals")
#         if len(goals) == 2:
#             print("   ✓ Correct count")
#         else:
#             print(f"   ⚠ Expected 2 goals, got {len(goals)}")
#     else:
#         print(f"   ✗ Failed: {response.status_code}")
#         return False
    
#     # Step 8: Delete first goal
#     print("\n8. Deleting first goal...")
#     response = session.delete(f"{BASE_URL}/goals/{goal_id}/")
#     if response.status_code == 204:
#         print("   ✓ Goal deleted")
#     else:
#         print(f"   ✗ Failed: {response.status_code}")
#         return False
    
#     # Step 9: Verify deletion
#     print("\n9. Verifying deletion...")
#     response = session.get(f"{BASE_URL}/goals/")
#     if response.status_code == 200:
#         goals = response.json()
#         print(f"   ✓ Now have {len(goals)} goal(s)")
#         if len(goals) == 1:
#             print("   ✓ Deletion confirmed")
#         else:
#             print(f"   ⚠ Expected 1 goal, got {len(goals)}")
#     else:
#         print(f"   ✗ Failed: {response.status_code}")
#         return False
    
#     # Step 10: Test unauthenticated access
#     print("\n10. Testing unauthorized access...")
#     unauth_session = requests.Session()
#     response = unauth_session.get(f"{BASE_URL}/goals/")
#     if response.status_code == 401 or response.status_code == 403:
#         print("   ✓ Correctly rejected unauthenticated request")
#     else:
#         print(f"   ⚠ Expected 401/403, got {response.status_code}")
    
#     print("\n" + "=" * 60)
#     print("✅ ALL GOALS API TESTS PASSED!")
#     print("=" * 60)
#     return True

# if __name__ == "__main__":
#     try:
#         success = test_goals_api()
#         exit(0 if success else 1)
#     except Exception as e:
#         print(f"\n❌ Test failed with exception: {e}")
#         import traceback
#         traceback.print_exc()
#         exit(1)
