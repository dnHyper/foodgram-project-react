from rest_framework import permissions


class IsAdminOrReadOnlyPermission(permissions.BasePermission):
    """Права, разрешающие читать всем, а редактировать администраторам"""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )


class IsAuthorOrAdminOrModeratorPermission(permissions.BasePermission):
    """Права, разрешающие редактировать пользователям и администрации"""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
            or request.user.is_authenticated
            or obj.author == request.user
        )
