import pytest
import factory
from factory.django import DjangoModelFactory
from article.models import Board
from article.providers import BoardAttrsProvider
from user.factories import UserFactory


factory.Faker.add_provider(BoardAttrsProvider)


class BoardFactory(DjangoModelFactory):
    class Meta:
        model = Board

    owner = factory.SubFactory(UserFactory)
    gerberFileName = "gerberfile.zip"
    gerberHash = "iahriug3wh8w9rfhhueigjhhiwof"
    attributes = factory.Faker("board_attributes")


VALID_BOARD_DATA = {
    "attributes": {
        "dimensionX": 30,
        "differentDesigns": 1
    }
}
