from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required

from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import User
from .address_management import Address, disable_old_default, set_new_default
from .serializers import UserSerializer, AddressSerializer


class UserList(generics.ListAPIView):
    """GET: Lists all registered users."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class UserDetails(generics.RetrieveDestroyAPIView):
    """GET: Returns details for current user.
    DELETE: Deletes current user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        current_user_pk = self.request.user.pk
        return get_object_or_404(User, pk=current_user_pk)


class AddressList(generics.ListCreateAPIView):
    """GET: Returns list of current user's addresses.
    POST: Saves new address to the database.
    """
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Returns a list of all the current user's addresses."""
        current_user = self.request.user
        return current_user.addresses.all()

    def perform_create(self, serializer):
        """Assures that a new address is saved with the calling user as owner."""
        serializer.save(user_id=self.request.user)


class AddressDetails(generics.RetrieveUpdateDestroyAPIView):
    """GET: Returns address details.
    PATCH: Updates existing address.
    DELETE: Deletes address from database.
    """
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user_id=self.request.user.pk)


class DefaultShippingAddressDetails(generics.RetrieveAPIView):
    """GET: Returns details of current user's default shipping address."""
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        current_user = self.request.user
        try:
            return current_user.addresses.get(is_shipping_default=True)
        except Address.DoesNotExist:
            return current_user.addresses.first()


class DefaultBillingAddressDetails(generics.RetrieveAPIView):
    """GET: Returns details of current user's default billing address."""
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        current_user = self.request.user
        try:
            return current_user.addresses.get(is_billing_default=True)
        except Address.DoesNotExist:
            return current_user.addresses.first()


@require_GET
@login_required
def change_address_default(request):
    """Changes a user's default shipping or billing address.
    The new default is given by the address id and the type URL parameter
    specifies the address type (shipping or billing)."""
    new_default_address_id = request.GET.get("address-id")
    address_type = request.GET.get("type")

    # Protect against malformed requests
    if new_default_address_id is None or address_type not in ["shipping", "billing"]:
        response_body = {"Error": "Query params not valid. Requires address-id and type (shipping or billing)."}
        return JsonResponse(status=400, data=response_body)

    current_user = request.user
    new_default_address_id = int(new_default_address_id)

    # Make sure current user owns the new default address
    if not current_user.addresses.filter(id=new_default_address_id):
        response_body = {"Error": "Address does not exist for this user."}
        return JsonResponse(status=404, data=response_body)

    disable_old_default(address_type, current_user)
    set_new_default(address_type, current_user, new_default_address_id)
    response_body = {"Success": f"Default {address_type} address changed successfully"}
    return JsonResponse(response_body)




