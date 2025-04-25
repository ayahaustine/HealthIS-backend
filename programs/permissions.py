from rest_framework import permissions

class IsCreatorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow read-only for all users
        if request.method in permissions.SAFE_METHODS:
            return True
        # Restrict write operations to creator
        return obj.created_by == request.user