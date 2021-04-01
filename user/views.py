from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.http import require_GET

from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import User
from .address_management import Address, disable_old_default, set_new_default
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
        """Returns a list of all the current user's addresses."""
        current_user = self.request.user
        return current_user.addresses.all()

    def perform_create(self, serializer):
        """Assures that a new address is saved with the calling user as owner."""
        serializer.save(user_id=self.request.user)


class DefaultShippingAddressDetails(generics.RetrieveAPIView):
    serializer_class = AddressSerializer

    def get_object(self):
        current_user = self.request.user
        try:
            return current_user.addresses.get(is_shipping_default=True)
        except Address.DoesNotExist:
            return current_user.addresses.first()


class DefaultBillingAddressDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AddressSerializer

    def get_object(self):
        current_user = self.request.user
        try:
            return current_user.addresses.get(is_billing_default=True)
        except Address.DoesNotExist:
            return current_user.addresses.first()


@require_GET()
def change_address_default(request):
    """Changes a user's default shipping or billing address.
    The new default is given by the address id and the type URL parameter
    specifies the address type (shipping or billing)."""
    new_default_address_id = request.GET.get("address_id")
    address_type = request.GET.get("type")

    # Protect against malformed requests
    if new_default_address_id is None or address_type not in ["shipping", "billing"]:
        return HttpResponseBadRequest("Query params not valid. Requires address_id and type (shipping or billing).")

    current_user = request.user
    new_default_address_id = int(new_default_address_id)

    # Make sure current user owns the new default address
    if not current_user.addresses.filter(id=new_default_address_id):
        return HttpResponseNotFound("Address does not exist for this user.")

    disable_old_default(address_type, current_user)
    set_new_default(address_type, current_user, new_default_address_id)

    return HttpResponse(f"Default {address_type} address changed successfully", status=200)





