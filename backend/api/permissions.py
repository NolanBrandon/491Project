"""
Custom permission classes for session-based authentication
"""
from rest_framework.permissions import BasePermission


class IsAuthenticatedWithSession(BasePermission):
    """
    Allow access only to authenticated users with valid sessions.
    """
    
    def has_permission(self, request, view):
        """
        Check if user is authenticated via session
        """
        return bool(
            request.user and 
            hasattr(request, 'session') and 
            request.session.get('user_id')
        )


class IsOwnerOrReadOnly(BasePermission):
    """
    Allow users to only edit their own resources.
    """
    
    def has_object_permission(self, request, view, obj):
        """
        Check if the user owns this object
        """
        # Read permissions are allowed to authenticated users
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        # Write permissions only for the owner
        if hasattr(obj, 'user'):
            return obj.user.id == request.session.get('user_id')
        elif hasattr(obj, 'id'):
            # For User objects themselves
            return str(obj.id) == request.session.get('user_id')
        
        return False
