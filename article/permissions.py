from rest_framework.permissions import BasePermission
from .models import Board


class IsBoardOwner(BasePermission):
    def has_permission(self, request, view):
        """Checks if a given user is the owner of a given board."""
        board_id = view.kwargs.get("pk")
        owner_id = Board.objects.get(pk=board_id).owner.pk
        return request.user.id == owner_id
