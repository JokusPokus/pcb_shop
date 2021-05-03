from django.db import transaction
from django.core.management.base import BaseCommand

from user.factories import UserFactory, AddressFactory
from article.factories import BoardFactory, ExternalBoardOptionsFactory, OfferedBoardOptionsFactory
from order.factories import OrderFactory


NUM_USERS = 100
NUM_BOARDS_PER_USER = 10
NUM_ADDRESSES_PER_USER = 5
NUM_OFFERED_BOARD_OPTIONS = 20

ADMIN_NAME = "admin"
ADMIN_EMAIL = "admin@gmail.com"
ADMIN_PASSWORD = "pcb_password"


class Command(BaseCommand):
    help = "Populate database with fake data."

    @transaction.atomic
    def create_user_data(self, num_users: int, num_boards_per_user: int, num_addresses_per_user: int):
        for _ in range(num_users):
            user = UserFactory()

            for _ in range(num_boards_per_user):
                BoardFactory(owner=user)

            for _ in range(num_addresses_per_user - 2):
                AddressFactory(user=user)

            default_shipping_address = AddressFactory(is_shipping_default=True)
            default_billing_address = AddressFactory(is_billing_default=True)

            OrderFactory(
                user=user,
                shipping_address=default_shipping_address,
                billing_address=default_billing_address
            )

    def handle(self, *args, **options):
        self.stdout.write(f"Creating superuser '{ADMIN_NAME}' ({ADMIN_EMAIL}) with password '{ADMIN_PASSWORD}'")
        UserFactory(
            username=ADMIN_NAME,
            email=ADMIN_EMAIL,
            password=ADMIN_PASSWORD,
            is_superuser=True,
            is_staff=True
        )

        self.stdout.write(f"Creating data for {NUM_USERS} users...")
        self.create_user_data(NUM_USERS, NUM_BOARDS_PER_USER, NUM_ADDRESSES_PER_USER)
        self.stdout.write(f"Creating data for {NUM_OFFERED_BOARD_OPTIONS} offered board options...")

        for _ in range(NUM_OFFERED_BOARD_OPTIONS):
            OfferedBoardOptionsFactory()
            ExternalBoardOptionsFactory()

        self.stdout.write("Done")
