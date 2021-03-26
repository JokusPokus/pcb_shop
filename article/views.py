from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import Board
from .serializers import BoardSerializer


class BoardList(generics.ListCreateAPIView):
    serializer_class = BoardSerializer

    def get_queryset(self):
        """
        Returns a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return Board.objects.filter(owner=user)
