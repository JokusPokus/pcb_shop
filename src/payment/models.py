from django.db import models
from order.models import Order


class PaymentMethod(models.Model):
    """Model for payment method."""
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)
    provider_name = models.CharField(max_length=100)
    fee = models.DecimalField(max_digits=6, decimal_places=2)
    sorter = models.PositiveIntegerField()

    class Meta:
        ordering = ['sorter']


class Payment(models.Model):
    """Model for payment."""
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)
    amount_paid = models.DecimalField(max_digits=6, decimal_places=2)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.DO_NOTHING)
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
