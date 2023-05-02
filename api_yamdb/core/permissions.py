from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """IsAdmin permission.
    Разрешает доступ к ресурсу, если пользователь аутентифицирован и является
    администратором или суперпользователем.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """IsAdmin permission.
    Разрешает доступ к ресурсу, если используется безопасный метод или в
    случае, когда пользователь аутентифицирован и является администратором или
    суперпользователем.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (request.user.is_admin or request.user.is_superuser)
        )


class IsAuthorModeratorAdminOrReadOnly(permissions.BasePermission):
    """IsAuthorModeratorAdminOrReadOnly permission.
    1) Разрешает доступ к ресурсу, если используется безопасный метод или в
    случае, когда пользователь аутентифицирован.
    2) Разрешает доступ к объекту в случаях, когда используется безопасный
    метод или пользователь - это автор объекта, имеет роль
    модератора, администратора или суперпользователя.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_admin
            or request.user.is_moderator
            or request.user.is_superuser
        )

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )
