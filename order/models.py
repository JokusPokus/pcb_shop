from django.db import models
from django.db.models import Model
from django.contrib.auth.models import User
import article.models
import user.models


# **********
# SHIPPING_METHOD
# **********
class ShippingMethod(Model):
    """Model for Sipping Method"""

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
class OrderState(Model):
    """Model for Order State"""

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)


# **********
# ORDER
# **********
class Order(Model):
    """Model for Order"""

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    shipping_method = models.ForeignKey(ShippingMethod, on_delete=models.DO_NOTHING)
    shipping_address = models.ForeignKey(Address, on_delete=models.DO_NOTHING)
    billing_address = models.ForeignKey(Address, on_delete=models.DO_NOTHING)
    value = models.FloatField()
    vat = models.FloatField()
    order_state = models.ForeignKey(OrderState, on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)


# **********
# ARTICLE2ORDER
# **********
class Article2Order(Model):
    """Model for Article 2 Order"""

    article = models.ForeignKey(Article, on_delete=models.DO_NOTHING)
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['order', 'article']
