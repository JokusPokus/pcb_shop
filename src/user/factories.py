import random
import factory
from factory.django import DjangoModelFactory
from .models import User, BasketItem
from .address_management import Address


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker("email")
    username = factory.SelfAttribute("email")
    password = factory.PostGenerationMethodCall('set_password', 'pcb_password')
    is_superuser = False
    is_staff = False
    is_active = True


class BasketItemFactory(DjangoModelFactory):
    pass


class AddressFactory(DjangoModelFactory):
    class Meta:
        model = Address

    receiver_first_name = factory.Faker("first_name")
    receiver_last_name = factory.Faker("last_name")
    street = factory.Faker("street_name")
    house_number = factory.Faker("building_number")
    zip_code = factory.Faker("postcode")
    city = factory.Faker("city")
    user = factory.SubFactory(UserFactory)
