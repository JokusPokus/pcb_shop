from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound

from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import User
from .address_management import Address
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


def change_address_default(request):
    """Changes a user's default shipping or billing address.
    The new default is given by the address id and the type URL parameter
    specifies the address type (shipping or billing)."""
    def disable_old_default(_type: str, _user: User):
        try:
            if _type == "shipping":
                current_default = _user.addresses.get(is_shipping_default=True)
                current_default.is_shipping_default = False
            else:
                current_default = _user.addresses.get(is_billing_default=True)
                current_default.is_billing_default = False
            current_default.save()
        except Address.DoesNotExist:
            pass

    def set_new_default(_type: str, _user: User, _id: int):
        new_default = current_user.addresses.get(id=_id)
        if _type == "shipping":
            new_default.is_shipping_default = True
        else:
            new_default.is_billing_default = True
        new_default.save()

    new_default_address_id = request.GET.get("address_id")
    address_type = request.GET.get("type")

    if new_default_address_id is None or address_type not in ["shipping", "billing"]:
        return HttpResponseBadRequest("Query params not valid. Requires address_id and type (shipping or billing).")

    current_user = request.user
    new_default_address_id = int(new_default_address_id)

    if not current_user.addresses.filter(id=new_default_address_id):
        return HttpResponseNotFound("Address does not exist for this user.")

    disable_old_default(address_type, current_user)
    set_new_default(address_type, current_user, new_default_address_id)

    return HttpResponse(f"Default {address_type} address changed successfully", status=200)





