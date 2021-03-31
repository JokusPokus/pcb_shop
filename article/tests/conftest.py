import pytest

from django.urls import reverse


VALID_BOARD_DATA = {
    "dimensionX": 100,
    "dimensionY": 100,
    "gerberFileName": "gerber.zip",
    "gerberHash": "blablub123",
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


@pytest.fixture
def create_boards_with_authenticated_user(authenticated_client):
    def create_board(num_boards=1):
        """Closure to create boards"""
        for _ in range(num_boards):
            response = authenticated_client.post(path=reverse("shop:board_list"), data=VALID_BOARD_DATA)
        return response
    return create_board


@pytest.fixture
def create_board_with_anonymous_user(client):
    response = client.post(path=reverse("shop:board_list"), data=VALID_BOARD_DATA)
    return response


@pytest.fixture(params=[key for key in VALID_BOARD_DATA])
def create_incomplete_board(authenticated_client, request):
    """Sends POST request to create a board where the :attr:
    information is missing and returns the response.
    """
    board_data = VALID_BOARD_DATA.copy()
    del board_data[request.param]
    _response = authenticated_client.post(path=reverse("shop:board_list"), data=board_data)
    return request.param, board_data, _response


@pytest.fixture()
def create_three_boards(authenticated_client):
    for _ in range(3):
        authenticated_client.post(path=reverse("shop:board_list"), data=VALID_BOARD_DATA)