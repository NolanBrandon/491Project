from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

# Create your tests here.

class HealthCheckTestCase(APITestCase):
    """
    Test cases for the health check endpoint.
    """
    
    def test_health_check_endpoint(self):
        """
        Test that the health check endpoint returns a successful response.
        """
        url = reverse('health_check')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'healthy')
        self.assertIn('message', response.data)
        self.assertIn('version', response.data)

    def test_api_info_endpoint(self):
        """
        Test that the API info endpoint returns correct information.
        """
        url = reverse('api_info')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'EasyFitness API')
        self.assertIn('version', response.data)
        self.assertIn('endpoints', response.data)