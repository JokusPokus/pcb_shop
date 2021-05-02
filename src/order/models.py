from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

from auditlog.registry import auditlog

from article.models import Article, Board
from user.models import BasketItem
from user.address_management import Address
from price.calculate_board_price import BoardPriceCalculator


class ShippingProvider(models.Model):
    """Model for Shipping Provider"""
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)


class ShippingMethod(models.Model):
    """Model for Shipping Method"""
    shipping_provider = models.ForeignKey(ShippingProvider, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
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
    items = models.JSONField(null=True, blank=True)
    shipping_method = models.ForeignKey(ShippingMethod, on_delete=models.DO_NOTHING)
    shipping_cost = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
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
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    vat = models.DecimalField(max_digits=6, decimal_places=2)
    order_state = models.ForeignKey(OrderState, on_delete=models.DO_NOTHING)
    payment_state = models.ForeignKey(PaymentState, on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """Ensured that shipping cost is equal to the current price
        of the chosen shipping method.
        """
        if not self.shipping_cost:
            self.shipping_cost = self.shipping_method.price
        super(Order, self).save(*args, **kwargs)


class Article2Order(models.Model):
    """Model for Article 2 Order"""
    article = models.ForeignKey(Article, on_delete=models.DO_NOTHING)
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
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
        order=order,
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
        item_list = []

        for basket_item in basket_items:
            order_item = create_order_item(basket_item, instance, calculator)
            order_item.save()
            item_list.append(get_board_attrs(basket_item))
            basket_item.delete()

        instance.items = item_list
        instance.save()


auditlog.register(ShippingProvider)
auditlog.register(ShippingMethod)
auditlog.register(OrderState)
auditlog.register(PaymentState)
auditlog.register(Order)
auditlog.register(Article2Order)
