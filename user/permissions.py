from rest_framework.permissions import BasePermission, IsAdminUser


class IsAdminOrCreateOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return IsAdminUser()

        return True


class IsAuthorized(BasePermission):
    def has_permission(self, request, view):
        return request.user.id == view.kwargs.get("pk")
