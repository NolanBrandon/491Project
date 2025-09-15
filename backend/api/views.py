from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse


@api_view(['GET'])
def health_check(request):
    """
    Simple health check endpoint to verify the API is running.
    """
    return Response({
        'status': 'healthy',
        'message': 'EasyFitness API is running successfully!',
        'version': '1.0.0'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def api_info(request):
    """
    Provides basic information about the API.
    """
    return Response({
        'name': 'EasyFitness API',
        'version': '1.0.0',
        'description': 'Backend API for the EasyFitness application',
        'endpoints': {
            'health': '/api/health/',
            'info': '/api/info/',
            'admin': '/admin/',
        }
    }, status=status.HTTP_200_OK)