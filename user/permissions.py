from rest_framework.permissions import BasePermission, IsAdminUser


class IsAdminOrCreateOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return IsAdminUser()

        return True


class IsAuthorized(BasePermission):
    def has_permission(self, request, view):
        print(request.user.id)
        print(type(request.user.id))
        print(view.kwargs.get("pk"))
        print(type(view.kwargs.get("pk")))
        return request.user.id == view.kwargs.get("pk")
