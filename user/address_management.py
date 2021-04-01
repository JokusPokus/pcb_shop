from django.db import models
from .models import User


class Address(models.Model):
    """Model for users' addresses."""
    receiver_first_name = models.CharField(max_length=30)
    receiver_last_name = models.CharField(max_length=40)
    address_extension = models.CharField(max_length=40, null=True, blank=True)
    street = models.CharField(max_length=40)
    house_number = models.CharField(max_length=8)
    zip_code = models.CharField(max_length=5)

    # Each address is necessarily linked to exactly one user
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses", default=1)

    is_shipping_default = models.BooleanField(default=False)
    is_billing_default = models.BooleanField(default=False)


def disable_old_default(_type: str, _user: User):
    """Utility to disable default status of a user's current default address.
    The _type parameter distinguishes billing and shipping addresses.
    """
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
    """Utility to set new default address of a given user.
    The _type parameter distinguishes billing and shipping addresses.
    The _id parameter refers to an existing address.
    """
    new_default = current_user.addresses.get(id=_id)
    if _type == "shipping":
        new_default.is_shipping_default = True
    else:
        new_default.is_billing_default = True
    new_default.save()