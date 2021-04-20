from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required

from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import User, BasketItem
from .address_management import Address, disable_old_default, set_new_default
from .serializers import UserSerializer, AddressSerializer, BasketItemSerializer


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
    """GET: Returns list of current user's addresses. If query parameters is_billing_default
    or is_shipping_default (not both at the same time) are added with the value "true",
    the respective default address is returned.

    POST: Saves new address to the database.
    """
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return list of addresses or default shipping/billing address,
        based on query parameters.
        """
        current_user = self.request.user

        for address_type in ["billing", "shipping"]:
            if self.request.query_params.get(f"is{address_type.capitalize()}Default") == "true":

                default_address = current_user.addresses.filter(**{f"is_{address_type}_default": True})
                if not default_address:
                    return JsonResponse(status=404, data={"Error": f"User has no default {address_type} address"})

                return default_address

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


@require_GET
@login_required
def change_address_default(request):
    """GET: Changes a user's default shipping or billing address.
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


class BasketItemList(generics.ListAPIView):
    serializer_class = BasketItemSerializer

    def get_queryset(self):
        user = self.request.user
        return BasketItem.objects.filter(owner=user)


class BasketItemDetails(generics.RetrieveDestroyAPIView):
    serializer_class = BasketItemSerializer

    def get_object(self):
        user = self.request.user
        basket_items = BasketItem.objects.filter(owner=user)
        article_pk = self.kwargs.get("article_pk")
        return get_object_or_404(basket_items, article=article_pk)
