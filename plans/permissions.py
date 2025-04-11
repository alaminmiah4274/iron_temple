from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Custom permission to only allow owners to access their payments."""

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsStaffUser(permissions.BasePermission):
    """
    Allows access only to staff users.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_staff
