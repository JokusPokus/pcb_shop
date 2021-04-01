from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import User
from .serializers import UserSerializer, AddressSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class UserDetails(generics.RetrieveDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser | IsAuthenticated]

    def get_object(self):
        current_user_pk = self.request.user.pk
        return get_object_or_404(User, pk=current_user_pk)


class AddressList(generics.ListCreateAPIView):
    serializer_class = AddressSerializer

    def get_queryset(self):
        current_user = self.request.user
        return current_user.address_set.all()


class DefaultShippingAddressDetails(generics.RetrieveAPIView):
    serializer_class = AddressSerializer

    def get_object(self):
        current_user = self.request.user
        return current_user.profile.default_shipping_address


class DefaultBillingAddressDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AddressSerializer

    def get_object(self):
        current_user = self.request.user
        return current_user.profile.default_billing_address
