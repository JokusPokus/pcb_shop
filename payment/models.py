from django.db import models
from django.db.models import Model
from order.models import Order

# **********
# PAYMENT_METHOD
# **********
class PaymentMethod(Model):
    """Model for payment method."""

    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    fee = models.FloatField()
    sorter = models.DecimalField()

    class Meta:
        ordering = ['sorter']


# **********
# PAYMENT
# **********
class Payment(Model):
    created = models.DateTimeField(auto_now_add=True)
    paymentMethod = models.ForeignKey(PaymentMethod, on_delete=models.DO_NOTHING, null=True)
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
