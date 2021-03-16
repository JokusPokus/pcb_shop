from django.db import models
from django.contrib.auth.models import User
from article.models import Article
from user.models import Address


class ShippingMethod(models.Model):
    """Model for Shipping Method"""
    name = models.CharField(max_length=100)
    price = models.FloatField()
    sorter = models.DecimalField()
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sorter']


class OrderState(models.Model):
    """Model for Order State"""
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)


class PaymentState(models.Model):
    """Model for Payment State"""
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)


class Order(models.Model):
    """Model for Order"""
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    shipping_method = models.ForeignKey(ShippingMethod, on_delete=models.DO_NOTHING)
    shipping_address = models.ForeignKey(
        Address,
        on_delete=models.DO_NOTHING,
        related_name='orders_shipping'
    )
    billing_address = models.ForeignKey(
        Address,
        on_delete=models.DO_NOTHING,
        related_name='orders_billing'
    )
    value = models.FloatField()
    vat = models.FloatField()
    order_state = models.ForeignKey(OrderState, on_delete=models.DO_NOTHING)
    payment_state = models.ForeignKey(PaymentState, on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)


class Article2Order(models.Model):
    """Model for Article 2 Order"""
    article = models.ForeignKey(Article, on_delete=models.DO_NOTHING)
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    unit_price = models.FloatField()
    quantity = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['order', 'article']
