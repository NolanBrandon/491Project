"""
Custom authentication classes for session-based authentication
"""
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import User


class SessionAuthentication(BaseAuthentication):
    """
    Custom session authentication that uses Django sessions
    and our custom User model.
    """
    
    def authenticate(self, request):
        """
        Authenticate the request using session data.
        Returns (user, None) if authenticated, or None if not.
        """
        # Check if user_id exists in session
        user_id = request.session.get('user_id')
        
        if not user_id:
            return None
        
        try:
            user = User.objects.get(id=user_id)
            return (user, None)  # DRF expects (user, auth) tuple
        except User.DoesNotExist:
            # Session references non-existent user, clear it
            request.session.flush()
            return None
    
    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the WWW-Authenticate
        header in a 401 Unauthenticated response.
        """
        return 'Session'
