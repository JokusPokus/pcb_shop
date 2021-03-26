from rest_framework.permissions import BasePermission
from .models import Board


class IsBoardOwner(BasePermission):
    def has_permission(self, request, view):
        board_id = view.kwargs.get("pk")
        owner_id = Board.objects.get(pk=board_id).owner.pk
        return request.user.id == owner_id
