from rest_framework import permissions


class IsModeratorOrAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.role == 'Moderator'
            or obj.owner == request.user
        )
