import factory
from factory.django import DjangoModelFactory
from .models import Order, ShippingMethod, OrderState, PaymentState
from user.factories import UserFactory, AddressFactory


class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order

    user = factory.SubFactory(UserFactory)
    items = factory.Faker("json")
    shipping_method = ShippingMethod.objects.get(pk=1)
    shipping_cost = factory.SelfAttribute("shipping_method.price")
    shipping_address = factory.SubFactory(AddressFactory)
    billing_address = factory.SubFactory(AddressFactory)
    amount = 15.99
    vat = 1.12
    order_state = OrderState.objects.get(name="received")
    payment_state = PaymentState.objects.get(name="pending")
