# from django.test import TestCase
# from django.contrib.auth import get_user_model
# from rest_framework.test import APIClient
# import time

# User = get_user_model()


# class APIEndpointPerformanceTests(TestCase):
#     """Test API endpoint response times."""
    
#     def setUp(self):
#         self.client = APIClient()
#         self.user = User.objects.create_user(
#             username='testuser',
#             password='testpass123',
#             email='test@example.com'
#         )
#         self.client.force_authenticate(user=self.user)
    
#     def test_authentication_performance(self):
#         """Login should complete in < 1 second."""
#         self.client.logout()
        
#         start = time.time()
#         response = self.client.post('/api/auth/login/', {
#             'username': 'testuser',
#             'password': 'testpass123'
#         })
#         duration = time.time() - start
        
#         self.assertEqual(response.status_code, 200)
#         self.assertLess(
#             duration, 1.0,
#             f"Login took {duration:.3f}s (threshold: 1s)"
#         )
#         print(f"✅ Login completed in {duration:.3f}s")
    
#     def test_dashboard_load_performance(self):
#         """Dashboard should load in < 3 seconds."""
        
#         start = time.time()
#         response = self.client.get('/api/dashboard/')
#         duration = time.time() - start
        
#         self.assertEqual(response.status_code, 200)
#         self.assertLess(
#             duration, 3.0,
#             f"Dashboard load took {duration:.3f}s (threshold: 3s)"
#         )
#         print(f"✅ Dashboard loaded in {duration:.3f}s")
