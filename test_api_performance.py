from django.test import TestCase
from rest_framework.test import APIClient
import time


class APIEndpointPerformanceTests(TestCase):
    """Test API endpoint response times."""

    def setUp(self):
        self.client = APIClient()

    def test_users_list_performance(self):
        """GET /users/ should respond in < 1 second."""
        start = time.time()
        response = self.client.get('/users/')
        duration = time.time() - start

        self.assertEqual(response.status_code, 200)
        self.assertLess(
            duration, 1.0,
            f"/users/ took {duration:.3f}s (threshold: 1s)"
        )
        print(f"✅ /users/ completed in {duration:.3f}s")

    def test_goals_list_performance(self):
        """GET /goals/ should respond in < 1 second."""
        start = time.time()
        response = self.client.get('/goals/')
        duration = time.time() - start

        self.assertEqual(response.status_code, 200)
        self.assertLess(
            duration, 1.0,
            f"/goals/ took {duration:.3f}s (threshold: 1s)"
        )
        print(f"✅ /goals/ completed in {duration:.3f}s")

    def test_health_endpoint_performance(self):
        """GET /health/ should respond in < 0.5 seconds."""
        start = time.time()
        response = self.client.get('/health/')
        duration = time.time() - start

        self.assertEqual(response.status_code, 200)
        self.assertLess(
            duration, 0.5,
            f"/health/ took {duration:.3f}s (threshold: 0.5s)"
        )
        print(f"✅ /health/ completed in {duration:.3f}s")
