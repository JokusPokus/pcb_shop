from django.db import models
from order.models import Order


class PaymentMethod(models.Model):
    """Model for payment method."""
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    fee = models.FloatField()
    sorter = models.PositiveIntegerField()

    class Meta:
        ordering = ['sorter']


class Payment(models.Model):
    """Model for payment."""
    created = models.DateTimeField(auto_now_add=True)
    value = models.FloatField()
    paymentMethod = models.ForeignKey(PaymentMethod, on_delete=models.DO_NOTHING)
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
