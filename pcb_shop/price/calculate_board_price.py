from random import randint


class BoardPriceCalculator:
    """A class that calculates a price for a given board configuration."""
    @staticmethod
    def calculate_price(board_attributes: dict) -> float:
        """Returns the current price for a given board configuration."""
        toy_price = randint(200, 1000) / 100
        return toy_price
