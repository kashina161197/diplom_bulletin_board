from rest_framework import permissions


class IsModer(permissions.BasePermission):
    """Проверяет, является ли пользователь администратором (модератором)"""

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moders").exists()


class IsOwner(permissions.BasePermission):
    """Проверяет, является ли пользователь владельцем объекта"""

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False


class IsUser(permissions.BasePermission):
    """Проверяет, является ли это профиль текущего пользователя"""

    def has_object_permission(self, request, view, obj):
        if obj == request.user:
            return True
        return False
