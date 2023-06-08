from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrSelfOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated or request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.user.is_admin or request.user == \
            obj.user or request.method in SAFE_METHODS
