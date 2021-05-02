from rest_framework.permissions import BasePermission, IsAdminUser


class IsAuthorized(BasePermission):
    def has_permission(self, request, view):
        return request.user.id == view.kwargs.get("pk")
