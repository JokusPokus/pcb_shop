import pytest
from typing import Dict, Optional, Callable
from django.shortcuts import reverse





@pytest.fixture
def valid_credentials() -> Dict:
    """Returns an example of valid user registration credentials"""
    return {
        "email": "charly@gmail.com",
        "password1": "SuperStrongPassword",
        "password2": "SuperStrongPassword"
    }


@pytest.fixture
def create_address(client, user) -> Callable:
    def _create_address(address_data: Optional[Dict] = None, anonymous: bool = False):
        """Closure to create address with given address data.
        If :anonymous: is set to False, the client will be authenticated.
        """
        if address_data is None:
            address_data = VALID_ADDRESS.copy()

        if anonymous and user.is_authenticated:
            client.logout()
        if not anonymous:
            client.force_login(user)

        response = client.post(path=reverse("user:address_list"), data=address_data)
        return response
    return _create_address


@pytest.fixture
def set_as_default(authenticated_client) -> Callable:
    def _set_as_default(address_type: str, address_id: int):
        """Closure to set address as default shipping or billing address."""
        path = reverse("user:change_address_default") + f"?address-id={address_id}&type={address_type}"
        response = authenticated_client.get(path=path)
        return response
    return _set_as_default


@pytest.fixture
def create_and_set_as_default(create_address, set_as_default) -> Callable:
    def _create_and_set_as_default(address_type: str, address_data: Optional[Dict] = None):
        """Closure for convenient address creation and default setting."""
        if address_data is None:
            address_data = VALID_ADDRESS

        response = create_address(address_data)
        address_id = response.json()["id"]

        set_as_default(address_type, address_id)
    return _create_and_set_as_default


@pytest.fixture
def update_address(client, user) -> Callable:
    def _update_address(address_id: int, address: Optional[Dict] = None, anonymous: bool = False, **kwargs):
        """Closure that updates an existing address.
        If :anonymous: is set to False, the client will be authenticated.
        """
        if address is None:
            address = VALID_ADDRESS.copy()

        if anonymous and user.is_authenticated:
            client.logout()
        if not anonymous:
            client.force_login(user)

        address.update(kwargs)

        # Use API to update address
        response = client.patch(
            path=reverse("user:address_details", args=[address_id]),
            data=address,
            content_type='application/json'
        )
        return response
    return _update_address


@pytest.fixture
def delete_address(client, user) -> Callable:
    def _delete_address(address_id: int, anonymous: bool = False):
        """Closure that deletes an existing address for a user.
        If :anonymous: is set to False, the client will be authenticated.
        """
        if anonymous and user.is_authenticated:
            client.logout()
        if not anonymous:
            client.force_login(user)

        # Use API to update address
        response = client.delete(
            path=reverse("user:address_details", args=[address_id]),
            content_type='application/json'
        )
        return response
    return _delete_address
