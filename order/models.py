from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

from article.models import Article, Board
from user.models import Address, BasketItem
from price.calculate_board_price import BoardPriceCalculator


class ShippingMethod(models.Model):
    """Model for Shipping Method"""
    name = models.CharField(max_length=100)
    price = models.FloatField()
    sorter = models.PositiveIntegerField()
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


def get_board_attrs(basket_item: BasketItem) -> dict:
    """Returns the board attributes of a given basket item."""
    board = Board.objects.get(pk=basket_item.article.pk)
    return board.attributes


def create_order_item(basket_item: BasketItem, order: Order, calculator: BoardPriceCalculator) -> Article2Order:
    """Creates an order item based on a given basket item.
    The order item is returned, but not saved in the database yet.
    """
    board_attrs = get_board_attrs(basket_item)
    unit_price = calculator.calculate_price(board_attrs)
    order_item = Article2Order(
        article=basket_item.article,
        order=instance,
        unit_price=unit_price,
        quantity=1
    )
    return order_item


@receiver(post_save, sender=Order)
def handle_order_items(sender, instance, created, **kwargs):
    """Takes care that upon Order creation, all the user's basket items are added
    to the order and are then deleted from the user's basket.
    """
    if created:
        basket_items = BasketItem.objects.filter(owner=instance.user)
        calculator = BoardPriceCalculator()

        for basket_item in basket_items:
            order_item = create_order_item(basket_item, instance, calculator)
            order_item.save()
            basket_item.delete()
