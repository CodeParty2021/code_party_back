from rest_framework import permissions


class IsOwnerOrReadOnlyPermission(permissions.BasePermission):
    def has_permission(
        self,
        request,
        view,
    ):
        if request.method == "POST":
            # 認証済みの場合True
            return bool(request.user.id)
        else:
            return True

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        # オブジェクト操作系は所有者のみ有効
        return obj.user == request.user


class IsStaffOrReadOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff

    def has_object_permission(self, request, view, obj) -> bool:
        return True
