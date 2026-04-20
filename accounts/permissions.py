# accounts/permissions.py
from rest_framework import permissions


class IsAdminRole(permissions.BasePermission):
    """
    Allows access only to users who have the custom ADMIN role,
    except for the '/users/me/' endpoint which is open to any authenticated user.
    """

    def has_permission(self, request, view):
        # 1. Reject unauthenticated requests immediately
        if not request.user or not request.user.is_authenticated:
            return False

        # 2. Djoser's '/users/me/' route uses the 'me' action.
        # We allow all logged-in users to access their own profile.
        if getattr(view, 'action', None) == 'me':
            return True

        # 3. For all other endpoints (/users/, /users/{id}/), enforce the ADMIN role
        return request.user.is_admin()