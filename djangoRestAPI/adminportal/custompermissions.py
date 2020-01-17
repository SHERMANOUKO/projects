from rest_framework import permissions
from adminportal.models import CustomUser

class RegistrationPermission(permissions.BasePermission):
    """Global permission check for creating user"""

    def has_permission(self, request, view):
        try:
            if 'is_superuser' in request.data:
                return false
            
            if 'user_type' not in request.data:
                return True

            if request.data['user_type'] == 'CARETAKER':
                return request.user and request.user.is_authenticated and request.user.user_type in ('ADMIN', 'AD', 'AGENT')
            elif request.data['user_type'] == 'AGENT':
                return request.user and request.user.is_authenticated and request.user.user_type in ('ADMIN', 'AD')
            elif request.data['user_type'] == 'ADMIN':
                return request.user and request.user.is_authenticated and request.user.is_superuser
            else:
                return True
        except:
            return False

class CustomPermission(permissions.BasePermission):
    """Global permission check for admin user"""

    def has_permission(self, request, view):
        try:
            user = CustomUser.objects.get(username=request.user)
            return request.user and request.user.is_authenticated and user.user_type in ('ADMIN', 'AD')
        except:
            return False

class CustomAgentPermission(permissions.BasePermission):
    """Global permission check for agent and admin user"""

    def has_permission(self, request, view):
        try:
            user = CustomUser.objects.get(username=request.user)
            return (
                request.user and
                request.user.is_authenticated and
                user.user_type in ('ADMIN', 'AD', 'AGENT')
            )
        except:
            return False

class CustomAgentCaretakerPermission(permissions.BasePermission):
    """Global permission check for caretaker and agent and admin user"""

    def has_permission(self, request, view):
        try:
            user = CustomUser.objects.get(username=request.user)
            return (
                request.user and request.user.is_authenticated and
                (
                    user.user_type in ('ADMIN', 'AD') or \
                    user.user_type == 'AGENT' or \
                    user.user_type == 'CARETAKER'
                )
            )
        except:
            return False
       