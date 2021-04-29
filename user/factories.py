import factory
from .models import User, BasketItem


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker("email")
    username = factory.SelfAttribute("email")
    password = factory.PostGenerationMethodCall('set_password', 'pcb_password')
    is_superuser = False
    is_staff = False
    is_active = True


class BasketItemFactory(factory.django.DjangoModelFactory):
    pass