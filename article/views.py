from django.http import Http404

from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .permissions import IsBoardOwner

from .models import Board, ArticleCategory, OfferedBoardOptions
from .serializers import BoardSerializer, OfferedBoardOptionsSerializer


class BoardList(generics.ListCreateAPIView):
    """Provides functionality to list all PCBs the calling user has
    created (GET) or to create a new PCB (POST).
    """
    serializer_class = BoardSerializer

    def get_queryset(self):
        """
        Returns a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return Board.objects.filter(owner=user)

    def perform_create(self, serializer):
        """Assures that the board is saved with the PCB category
        and the calling user as owner.
        """
        category = ArticleCategory.objects.get(name="PCB")
        serializer.save(owner=self.request.user, category=category)


class BoardDetails(generics.RetrieveAPIView):
    """Returns details for a specific PCB (GET)."""
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAdminUser | (IsAuthenticated & IsBoardOwner)]

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except Board.DoesNotExist:
            raise Http404


class BoardOptions(generics.RetrieveAPIView):
    """Returns all currently available attribute options for PCB board."""
    serializer_class = OfferedBoardOptionsSerializer

    def get_object(self):
        return OfferedBoardOptions.objects.first()
