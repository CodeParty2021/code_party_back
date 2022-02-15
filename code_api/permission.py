from rest_framework import permissions


class IsOwnerOrReadOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        # オブジェクト操作系は所有者のみ有効
        return obj.user == request.user
