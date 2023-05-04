from users.permission import (BasePermission, 
                              IsAdminUser, IsSuperUser, SAFE_METHODS, 
                              CustomIsAdminUser, IsAdminOrReadOnly, 
                              IsAuthorOrModeratorOrAdminOrReadOnly)


class IsSuperUser(permissions.IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class CustomIsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return bool(request.user and request.user.is_admin)
        return False


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS or request.user.is_authenticated and request.user.is_admin:
            return True
        return False


class IsAuthorOrModeratorOrAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )
