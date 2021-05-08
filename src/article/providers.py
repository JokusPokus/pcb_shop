import random
from faker.providers import BaseProvider


class BoardAttrsProvider(BaseProvider):
    """Custom Faker provider for board attributes."""
    def board_attributes(self):
        """Returns a random but valid set of board attributes."""
        dimensionX = random.randint(100, 500)
        differentDesigns = 1

        return {
            "dimensionX": dimensionX,
            "differentDesigns": differentDesigns
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
