import pytest

from django.shortcuts import reverse


VALID_ADDRESS = {
    "receiver_first_name": "Max",
    "receiver_last_name": "Mustermann",
    "street": "Musterstraße",
    "house_number": "99",
    "zip_code": "99999"
}

OTHER_VALID_ADDRESS = {
    "receiver_first_name": "Maxime",
    "receiver_last_name": "Musterfrau",
    "street": "Musterstraße",
    "house_number": "88",
    "zip_code": "88888"
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
    def _create_address(address_data=VALID_ADDRESS):
        """Closure to create address with given address data."""
        response = authenticated_client.post(path=reverse("user:address_list"), data=address_data)
        return response
    return _create_address


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


@pytest.fixture(params=["shipping", "billing"])
def create_and_set_as_default(request, create_address, authenticated_client):
    def _create_and_set_as_default(address_data):
        """Closure to create address and then set it as default shipping or billing address."""
        create_response = create_address(address_data)

        address_id = create_response.json()["id"]
        path = reverse("user:change_address_default") + f"?address_id={address_id}&type={request.param}"
        response = authenticated_client.get(path=path)
        return response
    return _create_and_set_as_default
