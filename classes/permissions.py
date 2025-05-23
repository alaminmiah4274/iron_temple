from rest_framework import permissions


class AdminOrReadOnlyFitnessClass(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(
            request.user and (request.user.is_superuser or request.user.is_staff)
        )
