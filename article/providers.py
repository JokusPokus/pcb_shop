import random
from faker.providers import BaseProvider


class BoardAttrsProvider(BaseProvider):
    """Custom Faker provider for board attributes."""
    def board_attributes(self):
        """Returns a random but valid set of board attributes."""
        dimensionX = random.randint(100, 600)
        dimensionY = random.randint(100, 600)
        castellated_holes = random.choice(["yes", "no"])
        different_designs = 1
        quantity = random.choice([1, 2, 3, 4, 5, 10, 20, 50, 100])

        return {
            "dimensionX": dimensionX,
            "dimensionY": dimensionY,
            "castellatedHoles": castellated_holes,
            "differentDesigns": different_designs,
            "quantity": quantity
        }
