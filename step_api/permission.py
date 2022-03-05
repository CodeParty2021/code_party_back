import imp
from rest_framework import permissions

from users.models import User


class IsStuffOrReadOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_stuff

    def has_object_permission(self, request, view, obj) -> bool:
        return request.user.is_stuff
