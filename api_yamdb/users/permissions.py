from rest_framework import permissions


class UserRoleIsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated
            and request.user.role == 'admin'
            or request.user.is_superuser
        )
