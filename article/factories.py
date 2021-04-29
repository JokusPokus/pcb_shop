import factory
from .models import Board, ExternalShop, ExternalBoardOptions, OfferedBoardOptions
from .providers import BoardAttrsProvider
from user.factories import UserFactory


factory.Faker.add_provider(BoardAttrsProvider)


class BoardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Board

    owner = factory.SubFactory(UserFactory)
    gerberFileName = "gerberfile.zip"
    gerberHash = "iahriug3wh8w9rfhhueigjhhiwof"
    attributes = factory.Faker("board_attributes")
