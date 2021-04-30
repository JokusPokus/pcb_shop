import factory
from factory.django import DjangoModelFactory
from .models import Order, Article2Order, ShippingMethod, OrderState, PaymentState
from user.factories import UserFactory


class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order

    user = factory.SubFactory(UserFactory)
    items = factory.Faker("dict")
    shipping_method = ShippingMethod.objects.get(pk=1)
    shipping_cost = factory.SelfAttribute("shipping_method__price")
    shipping_address = factory.SubFactory(AddressFactory)
    billing_address = factory.SubFactory(AddressFactory)
    amount = 15.99
    vat = 1.12
    order_state = OrderState.objects.get(name="received")
    payment_state = PaymentState.objects.get(name="pending")
