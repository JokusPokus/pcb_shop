import pytest
import json

from django.urls import reverse

from typing import Optional, Dict, Callable


VALID_BOARD_DATA = {
    "gerberFileName": "gerber.zip",
    "gerberHash": "blablub123",
    "attributes": {
        "dimensionX": 100,
        "dimensionY": 100,
        "differentDesigns": 1,
        "layers": 3,
        "deliveryFormat": "Single PCB",
        "thickness": 1.6,
        "color": "Red",
        "surfaceFinish": "no",
        "copperWeight": 2,
        "goldFingers": "no",
        "castellatedHoles": "no",
        "removeOrderNum": "yes",
        "confirmProdFile": "yes",
        "flyingProbeTest": "no"
    }
}


@pytest.fixture
def create_boards(client, user) -> Callable:
    def _create_boards(data: Optional[Dict] = None, num_boards: int = 1, anonymous: bool = False):
        """Closure to create boards. If anonymous is true, the client is
        not authenticated.
        """
        if data is None:
            data = VALID_BOARD_DATA.copy()
        else:
            data = data.copy()

        data["attributes"] = json.dumps(data["attributes"])

        if not anonymous:
            client.force_login(user)

        for _ in range(num_boards):
            response = client.post(path=reverse("shop:board_list"), data=data)

        return response if num_boards == 1 else None
    return _create_boards


@pytest.fixture
def choice_attribute():
    return {
        "choices": [1, 2, 3]
    }


@pytest.fixture
def range_attribute():
    return {
        "range": {
            "min": 10,
            "max": 100,
        }
    }
