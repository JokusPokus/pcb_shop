from django.db import models
from django.contrib.auth.models import User
import article.models
import user.models
from user.models import Address


# **********
# SHIPPING_METHOD
# **********
class ShippingMethod(models.Model):
    """Model for Shipping Method"""
    name = models.CharField(max_length=100)
    price = models.FloatField()
    sorter = models.DecimalField()
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sorter']


# **********
# ORDER_STATE
# **********
class OrderState(models.Model):
    """Model for Order State"""
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)


# **********
# PAYMENT_STATE
# **********
class PaymentState(models.Model):
    """Model for Pyment State"""
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)


# **********
# ORDER
# **********
class Order(models.Model):
    """Model for Order"""
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    shipping_method = models.ForeignKey(ShippingMethod, on_delete=models.DO_NOTHING)
    shipping_address = models.ForeignKey(Address, on_delete=models.DO_NOTHING)
    billing_address = models.ForeignKey(Address, on_delete=models.DO_NOTHING)
    value = models.FloatField()
    vat = models.FloatField()
    order_state = models.ForeignKey(OrderState, on_delete=models.DO_NOTHING)
    payment_state = models.ForeignKey(PaymentState, on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)


# **********
# ARTICLE2ORDER
# **********
class Article2Order(models.Model):
    """Model for Article 2 Order"""
    article = models.ForeignKey(Article, on_delete=models.DO_NOTHING)
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['order', 'article']
