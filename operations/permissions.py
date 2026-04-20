from rest_framework import permissions


class IsAdminOrAssignedAgent(permissions.BasePermission):
    """
    Object-level permission to only allow admins or the assigned field agent to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_admin():
            return True

        # If they are a field agent, they must be the one assigned to this field
        return obj.agent == request.user