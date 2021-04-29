import factory
from factory.django import DjangoModelFactory
from .models import User, BasketItem


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
