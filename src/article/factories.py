import factory
from factory.django import DjangoModelFactory
from .models import Board, ExternalShop, ExternalBoardOptions, OfferedBoardOptions
from .providers import BoardAttrsProvider
from src.user.factories import UserFactory


factory.Faker.add_provider(BoardAttrsProvider)


class BoardFactory(DjangoModelFactory):
    class Meta:
        model = Board

    owner = factory.SubFactory(UserFactory)
    gerberFileName = "gerberfile.zip"
    gerberHash = "iahriug3wh8w9rfhhueigjhhiwof"
    attributes = factory.Faker("board_attributes")


class ExternalBoardOptionsFactory(DjangoModelFactory):
    class Meta:
        model = ExternalBoardOptions

    external_shop = ExternalShop.objects.get(name="Example PCB Shop")
    attribute_options = factory.Faker("attribute_options")


class OfferedBoardOptionsFactory(DjangoModelFactory):
    class Meta:
        model = OfferedBoardOptions

    attribute_options = factory.Faker("attribute_options")
