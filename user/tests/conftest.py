import pytest
from typing import Dict, Optional
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

INVALID_ADDRESS_FIELDS = [
    (pytest.param({"zip_code": "1234"}, id="Zip too short")),
    (pytest.param({"zip_code": "123456"}, id="Zip too long")),
    (pytest.param({"receiver_first_name": "a" * 100}, id="Name too long")),
    (pytest.param({"house_number": "1000000 c"}, id="House number too long"))
]


@pytest.fixture
def valid_credentials():
    return {
        "email": "charly@gmail.com",
        "password1": "SuperStrongPassword",
        "password2": "SuperStrongPassword"
    }


@pytest.fixture
def create_address(client, user):
    def _create_address(address_data: Optional[Dict] = None, anonymous: bool = False):
        """Closure to create address with given address data."""
        if address_data is None:
            address_data = VALID_ADDRESS.copy()

        if not anonymous:
            client.force_login(user)

        response = client.post(path=reverse("user:address_list"), data=address_data)
        return response
    return _create_address


@pytest.fixture(params=["shipping", "billing"])
def set_as_default(request, authenticated_client):
    def _set_as_default(address_id):
        """Closure to create address and then set it as default shipping or billing address."""
        path = reverse("user:change_address_default") + f"?address-id={address_id}&type={request.param}"
        response = authenticated_client.get(path=path)
        return response
    return _set_as_default


@pytest.fixture
def create_and_set_as_default(create_address, set_as_default):
    def _create_and_set_as_default(address_data: dict = VALID_ADDRESS):
        response = create_address(address_data)
        address_id = response.json()["id"]

        set_as_default(address_id)
    return _create_and_set_as_default


@pytest.fixture(params=["shipping", "billing"])
def set_non_existing_address_as_default(request, authenticated_client):
    ADDRESS_ID = 9999
    path = reverse("user:change_address_default") + f"?address-id={ADDRESS_ID}&type={request.param}"
    response = authenticated_client.get(path=path)
    return response


@pytest.fixture
def update_address(create_address, authenticated_client):
    def _update_address(address_id: int, address=None, **kwargs):
        """Closure to creates a new address for authenticated user, the updates that address."""
        if address is None:
            address = VALID_ADDRESS.copy()
        address.update(kwargs)

        # Use API to update address
        response = authenticated_client.patch(
            path=reverse("user:address_details", args=[address_id]),
            data=address,
            content_type='application/json'
        )
        return response
    return _update_address


def create_address_and_update_with_invalid_field(authenticated_client, updated_address):
    response = create_address()
    address_id = response.json()["id"]
    updated_address["invalid_field"] = ""

    response = authenticated_client.patch(
        path=reverse("user:address_details", args=[ADDRESS_ID]),
        data=updated_address,
        content_type='application/json'
    )
    return response
