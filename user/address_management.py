from django.db import models
from .models import User


class Address(models.Model):
    """Model for users' addresses."""
    receiver_first_name = models.CharField(max_length=30, default="Max")
    receiver_last_name = models.CharField(max_length=40, default="Mustermann")
    street = models.CharField(max_length=40, default="Musterstraße")
    additional_line = models.CharField(max_length=40, null=True, blank=True)
    house_number = models.CharField(max_length=8, default="9999")
    zip_code = models.CharField(max_length=5, default="99999")

    # Each address is necessarily linked to exactly one user
    user = models.ForeignKey(User, on_delete=models.CASCADE)
