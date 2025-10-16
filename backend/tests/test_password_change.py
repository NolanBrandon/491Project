# #!/usr/bin/env python3
# """Test password change endpoint"""
# import requests
# import json

# BASE_URL = "http://localhost:8000/api"

# # First, create a user and get their session
# print("Creating test user...")
# user_data = {
#     "username": "changetest_user",
#     "email": "changetest@example.com",
#     "password": "OldPass123!",
#     "password_confirm": "OldPass123!",
#     "gender": "other"
# }

# session = requests.Session()
# response = session.post(f"{BASE_URL}/users/", json=user_data)

# if response.status_code == 201:
#     user = response.json()['user']
#     user_id = user['id']
#     print(f"✅ User created: {user['username']} (ID: {user_id})")

#     # Test password change
#     print("\nTesting password change...")
#     change_data = {
#         "old_password": "OldPass123!",
#         "new_password": "NewSecurePass456!"
#     }

#     response = session.post(f"{BASE_URL}/users/{user_id}/change_password/", json=change_data)

#     if response.status_code == 200:
#         print("✅ Password changed successfully!")
#         print(f"Response: {response.json()}")

#         # Try logging in with new password
#         print("\nTesting login with new password...")
#         login_response = requests.post(f"{BASE_URL}/users/login/", json={
#             "username": "changetest_user",
#             "password": "NewSecurePass456!"
#         })

#         if login_response.status_code == 200:
#             print("✅ Login with new password successful!")

#             # Try old password (should fail)
#             print("\nTesting old password (should fail)...")
#             old_login = requests.post(f"{BASE_URL}/users/login/", json={
#                 "username": "changetest_user",
#                 "password": "OldPass123!"
#             })

#             if old_login.status_code == 401:
#                 print("✅ Old password correctly rejected!")
#                 print("\n🎉 Password change functionality working perfectly with secure hashing!")
#             else:
#                 print(f"❌ Old password still works (status: {old_login.status_code})")
#         else:
#             print(f"❌ Login with new password failed: {login_response.text}")
#     else:
#         print(f"❌ Password change failed: {response.text}")
# else:
#     print(f"❌ User creation failed: {response.text}")
