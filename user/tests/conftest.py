import pytest

from django.shortcuts import reverse


VALID_ADDRESS = {
    "receiver_first_name": "Max",
    "receiver_last_name": "Mustermann",
    "street": "Musterstraße",
    "house_number": "99",
    "zip_code": "99999"
}


@pytest.fixture
def valid_credentials():
    return {
        "email": "charly@gmail.com",
        "password1": "SuperStrongPassword",
        "password2": "SuperStrongPassword"
    }


@pytest.fixture
def create_address(authenticated_client):
    response = authenticated_client.post(path=reverse("user:address_list"), data=VALID_ADDRESS)
    return response


@pytest.fixture
def create_address_with_anonymous_user(client):
    response = client.post(path=reverse("user:address_list"), data=VALID_ADDRESS)
    return response


@pytest.fixture(params=[key for key in VALID_ADDRESS])
def create_incomplete_address(authenticated_client, request):
    """Sends POST request to create an address where the :request.param:
    information is missing and returns the response.
    """
    address_data = VALID_ADDRESS.copy()
    del address_data[request.param]
    _response = authenticated_client.post(path=reverse("user:address_list"), data=address_data)
    return request.param, address_data, _response
