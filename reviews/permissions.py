from rest_framework import permissions


class IsReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True


class IsWriteOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_active)
