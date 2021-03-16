from rest_framework.permissions import BasePermission


class IsAdminOrCreateOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return request.user.is_staff

        return True
