from django.http import JsonResponse

from .calculate_board_price import BoardPriceCalculator


def calculate_board_price(request):
    attributes = dict(request.GET)
    if not attributes:
        return JsonResponse({"detail": "No board attributes were provided as query params"})

    price_calculator = BoardPriceCalculator()
    price = price_calculator.calculate_price(attributes)
    return JsonResponse({"price": price})
