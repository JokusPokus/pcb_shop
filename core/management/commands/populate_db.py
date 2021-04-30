from django.db import transaction
from django.core.management.base import BaseCommand

from user.factories import UserFactory, AddressFactory
from article.factories import BoardFactory, ExternalBoardOptionsFactory, OfferedBoardOptionsFactory
from order.factories import OrderFactory


NUM_USERS = 100
NUM_BOARDS_PER_USER = 10
NUM_ADDRESSES_PER_USER = 5


class Command(BaseCommand):
    help = "Populate database with fake data."

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Creating data...")

        for _ in range(NUM_USERS):
            user = UserFactory()

            for _ in range(NUM_BOARDS_PER_USER):
                BoardFactory(owner=user)

            for _ in range(NUM_ADDRESSES_PER_USER):
                AddressFactory(user=user)
