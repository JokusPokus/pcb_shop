import json

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .calculate_board_price import BoardPriceCalculator


@require_POST
def calculate_board_price(request):
    body_unicode = request.body.decode('utf-8')
    attributes = json.loads(body_unicode)
    if not attributes:
        return JsonResponse({"detail": "No board attributes were provided as query params"})

    price_calculator = BoardPriceCalculator()
    price = price_calculator.calculate_price(attributes)
    return JsonResponse({"price": price})
