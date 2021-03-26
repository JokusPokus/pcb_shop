from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .permissions import IsBoardOwner

from .models import Board, ArticleCategory
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

    def perform_create(self, serializer):
        category = ArticleCategory.objects.get(name="PCB")
        serializer.save(owner=self.request.user, category=category)


class BoardDetails(generics.RetrieveAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAdminUser | (IsAuthenticated & IsBoardOwner)]

