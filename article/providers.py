import random
from faker.providers import BaseProvider


class BoardAttrsProvider(BaseProvider):
    """Custom Faker provider for board attributes."""
    def board_attributes(self):
        """Returns a random but valid set of board attributes."""
        dimensionX = random.randint(100, 600)
        dimensionY = random.randint(100, 600)
        castellated_holes = random.choice(["yes", "no"])
        num_designs = 1
        quantity = random.choice([1, 2, 3, 4, 5, 10, 20, 50, 100])

        return {
            "dimensionX": dimensionX,
            "dimensionY": dimensionY,
            "castellatedHoles": castellated_holes,
            "num_designs": num_designs,
            "quantity": quantity
        }

    def attribute_options(self):
        """Returns a set of board options."""
        return {
            "quantity": {
                "choices": sorted([random.randint(1, 100) for _ in range(10)])
            },
            "dimensionX": {
                "range": {
                    "min": random.randint(5, 10),
                    "max": random.randint(1000, 2000)
                }
            },
            "dimensionY": {
                "range": {
                    "min": random.randint(5, 10),
                    "max": random.randint(1000, 2000)
                }
            },
            "num_designs": {
                "choices": list(range(1, random.randint(2, 4)))
            },
            "castellated_holes": {
                "choices": ["yes", "no"]
            }
        }
