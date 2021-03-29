from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import User
from .serializers import UserSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class UserDetails(generics.RetrieveDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser | IsAuthenticated]

    def get_queryset(self):
        current_user_id = self.request.user.id
        return User.objects.get(pk=current_user_id)
