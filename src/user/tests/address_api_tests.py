import pytest

from django.urls import reverse

from . import VALID_ADDRESS_DATA, OTHER_VALID_ADDRESS

from user.address_management import Address
from user.factories import AddressFactory


@pytest.mark.django_db
class TestAddressCreationSuccess:
    def test_correct_http_response_and_inserted_into_db(self, authenticated_client, user):
        """GIVEN valid address and an authenticated user

        WHEN that user tries to save the address

        THEN a 201 status code is returned and the address is
        inserted into the database with defaults set to false.
        """
        response = authenticated_client.post(path=reverse("user:address_list"), data=VALID_ADDRESS_DATA)
        assert response.status_code == 201

        # Address is inserted into database and linked to the correct user
        assert user.addresses.filter(id=address_id, **VALID_ADDRESS_DATA).exists()

        # Billing and shipping defaults are set to false
        address = Address.objects.get(id=address_id)
        assert not address.is_shipping_default
        assert not address.is_billing_default


@pytest.mark.django_db
class TestAddressCreationFailure:
    def test_anonymous_user_is_handled_correctly(self, client):
        """GIVEN valid address data and an anonymous user

        WHEN that user tries to create the address

        THEN a 403 status code is returned and the address
        is not inserted into the database.
        """
        response = client.post(path=reverse("user:address_list"), data=VALID_ADDRESS_DATA)
        assert response.status_code == 403
        assert not Address.objects.filter(**VALID_ADDRESS_DATA).exists()

    @pytest.mark.parametrize("missing_attribute", [attribute for attribute in VALID_ADDRESS_DATA])
    def test_incomplete_address_is_handled_correctly(self, missing_attribute, authenticated_client):
        """GIVEN incomplete address data and an authenticated user

        WHEN that user tries to create the address

        THEN a 400 status code is returned and the address is not
        inserted into the database.
        """
        address_data = VALID_ADDRESS_DATA.copy()
        del address_data[missing_attribute]

        response = authenticated_client.post(path=reverse("user:address_list"), data=address_data)
        assert response.status_code == 400
        assert not Address.objects.filter(**address_data).exists()

    @pytest.mark.parametrize("invalid_field", [
        (pytest.param({"zip_code": "1234"}, id="Zip too short")),
        (pytest.param({"zip_code": "123456"}, id="Zip too long")),
        (pytest.param({"receiver_first_name": "a" * 100}, id="Name too long")),
        (pytest.param({"house_number": "1000000 c"}, id="House number too long"))
    ])
    def test_invalid_address_field_throws_error(self, invalid_field, authenticated_client):
        """GIVEN an authenticated user

        WHEN that user tries to create an address with (partially) invalid data

        THEN the correct Http error is returned and the address is
        not inserted into the database.
        """
        invalid_address = {**VALID_ADDRESS_DATA, **invalid_field}
        response = authenticated_client.post(path=reverse("user:address_list"), data=invalid_address)
        assert response.status_code == 400
        assert not Address.objects.filter(**invalid_address).exists()


@pytest.mark.django_db
class TestAddressListSuccess:
    def test_only_owned_addresses_are_listed(self, authenticated_client, user, other_user):
        """GIVEN an authenticated user with several existing addresses

        WHEN the user requests a list of her addresses

        THEN all her addresses are present, but none of the addresses
        not owned by her.
        """
        owned_address_ids = set()

        NUM_OWNED_ADDRESSES = 3
        for _ in range(NUM_OWNED_ADDRESSES):
            address = AddressFactory(user=user)
            owned_address_ids.add(address.id)

        NUM_NON_OWNED_ADDRESSES = 3
        for _ in range(NUM_NON_OWNED_ADDRESSES):
            AddressFactory(user=other_user)

        response = authenticated_client.get(path=reverse("user:address_list"))
        assert response.status_code == 200

        # Returned addresses contain owned addresses but not non-owned addresses
        response_body = response.json()
        returned_address_ids = {address["id"] for address in response_body}
        assert owned_address_ids == returned_address_ids


@pytest.mark.django_db
class TestAddressListFailure:
    def test_anonymous_user_cannot_get_address_list(self, client):
        """GIVEN an anonymous user

        WHEN she tries to request a list of addresses

        THEN the request is rejected and the correct HTTP response is returned."""
        response = client.get(path=reverse("user:address_list"))
        assert response.status_code == 403

    @pytest.mark.xfail
    def test_user_cannot_create_address_that_already_exists(self, authenticated_client, user):
        """GIVEN an authenticated user with an existing address

        WHEN that user tries to create an address with the same data

        THEN this is rejected and a 400 HTTP response is returned."""
        Address.objects.create(user=user, **VALID_ADDRESS_DATA)
        response = authenticated_client.post(path=reverse("user:address_list"), data=VALID_ADDRESS_DATA)
        assert response.status_code == 400
        assert Address.objects.filter(**VALID_ADDRESS_DATA).count() == 1


@pytest.mark.django_db
class TestAddressUpdateSuccess:
    def test_correct_http_response_and_db_update(self, authenticated_client, user):
        """GIVEN an authenticated user with an existing address

        WHEN the user updates a part of that address

        THEN the correct Http response is returned and the address is
        updated in the database.
        """
        address = Address.objects.create(user=user, **VALID_ADDRESS_DATA)

        UPDATED_ZIP_CODE = "12345"
        updated_address_data = {**VALID_ADDRESS_DATA, "zip_code": UPDATED_ZIP_CODE}

        response = authenticated_client.patch(
            path=reverse("user:address_details", args=[address.id]),
            data=updated_address_data,
            content_type='application/json'
        )
        assert response.status_code == 200
        assert user.addresses.get(id=address.id).zip_code == UPDATED_ZIP_CODE


@pytest.mark.django_db
class TestAddressUpdateFailure:
    def test_updating_non_existing_address_throws_404(self, authenticated_client):
        """GIVEN an authenticated user

        WHEN the user tries to update a non-existing address

        THEN the correct Http error code is returned.
        """
        NON_EXISTING_ADDRESS_ID = 9999
        response = authenticated_client.patch(
            path=reverse("user:address_details", args=[NON_EXISTING_ADDRESS_ID]),
            data=VALID_ADDRESS_DATA,
            content_type='application/json'
        )
        assert response.status_code == 404

    @pytest.mark.parametrize("invalid_field", [
        (pytest.param({"zip_code": "1234"}, id="Zip too short")),
        (pytest.param({"zip_code": "123456"}, id="Zip too long")),
        (pytest.param({"receiver_first_name": "a" * 100}, id="Name too long")),
        (pytest.param({"house_number": "1000000 c"}, id="House number too long"))
    ])
    def test_updating_address_with_invalid_data_throws_error(self, invalid_field, authenticated_client, user):
        """GIVEN an authenticated user

        WHEN the user tries to update an existing address with invalid data

        THEN the correct Http error code is returned.
        """
        address = Address.objects.create(user=user, **VALID_ADDRESS_DATA)
        invalid_address_update = {**VALID_ADDRESS_DATA, **invalid_field}

        response = authenticated_client.patch(
            path=reverse("user:address_details", args=[address.id]),
            data=invalid_address_update,
            content_type='application/json'
        )
        assert response.status_code == 400

    def test_anonymous_user_cannot_update_address(self, client, user):
        """GIVEN an anonymous user

        WHEN the user tries to update an existing address

        THEN permission is denied and the correct HTTP error code is returned.
        """
        address = Address.objects.create(user=user, **VALID_ADDRESS_DATA)
        updated_address_data = {**VALID_ADDRESS_DATA, "zip_code": "12345"}
        response = client.patch(
            path=reverse("user:address_details", args=[address.id]),
            data=updated_address_data,
            content_type='application/json'
        )
        assert response.status_code == 403


@pytest.mark.django_db
class TestAddressDeletionSuccess:
    def test_correct_http_response_and_address_is_deleted(self, authenticated_client, user):
        """GIVEN an authenticated user with an existing address

        WHEN the user deletes that address

        THEN the correct HTTP response is returned and the address
        is deleted from the database.
        """
        address = Address.objects.create(user=user, **VALID_ADDRESS_DATA)

        response = authenticated_client.delete(
            path=reverse("user:address_details", args=[address.id]),
            content_type='application/json'
        )
        assert response.status_code == 204
        assert not user.addresses.filter(id=address.id).exists()


@pytest.mark.django_db
class TestAddressDeletionFailure:
    def test_anonymous_user_cannot_delete_address(self, client, user):
        """GIVEN an anonymous user

        WHEN the user tries to delete an existing address

        THEN permission is denied and the correct Http error code is returned.
        """
        address = Address.objects.create(user=user, **VALID_ADDRESS_DATA)

        response = client.delete(
            path=reverse("user:address_details", args=[address.id]),
            content_type='application/json'
        )
        assert response.status_code == 403

    def test_deleting_non_existing_address_throws_404(self, authenticated_client):
        """GIVEN an authenticated user

        WHEN the user tries to delete a non-existing address

        THEN the correct Http error code is returned.
        """
        NON_EXISTING_ADDRESS_ID = 9999
        response = authenticated_client.delete(
            path=reverse("user:address_details", args=[NON_EXISTING_ADDRESS_ID]),
            content_type='application/json'
        )
        assert response.status_code == 404


@pytest.mark.django_db
class TestAddressDefaultChangeSuccess:
    @pytest.mark.parametrize("address_type", ["shipping", "billing"])
    def test_default_is_changed_correctly(self, address_type, authenticated_client, user):
        """GIVEN an authenticated user with an existing address

        WHEN the user sets that address as the new shipping or billing
        default address

        THEN she receives a 200 Http response with a success message."""
        # Create non-default address
        first_address = Address.objects.create(
            user=user,
            is_shipping_default=False,
            is_billing_default=False,
            **VALID_ADDRESS_DATA
        )

        # Create default address
        second_address = Address.objects.create(
            user=user,
            is_shipping_default=True,
            is_billing_default=True,
            **OTHER_VALID_ADDRESS
        )

        # Change default from second to first address via API
        url = reverse("user:change_address_default") + f"?address-id={first_address.id}&type={address_type}"
        response = authenticated_client.get(path=url)
        assert response.status_code == 200

        first_address.refresh_from_db()
        second_address.refresh_from_db()

        # First address is new default
        assert getattr(first_address, f"is_{address_type}_default")

        # Second address is not the default anymore
        assert not getattr(second_address, f"is_{address_type}_default")


@pytest.mark.django_db
class TestAddressDefaultChangeFailure:
    @pytest.mark.parametrize("address_type", ["shipping", "billing"])
    def test_handle_non_existing_address_as_default(self, address_type, authenticated_client, user):
        """GIVEN an authenticated user

        WHEN the user tries to set an address that does not exist
        as her new shipping or billing default address

        THEN the correct error is thrown and the old default
        is not affected."""
        default_address = Address.objects.create(
            user=user,
            is_shipping_default=True,
            is_billing_default=True,
            **OTHER_VALID_ADDRESS
        )

        # Try to change default to non-existing address
        NON_EXISTING_ADDRESS_ID = 9999
        url = reverse("user:change_address_default") + f"?address-id={NON_EXISTING_ADDRESS_ID}&type={address_type}"
        response = authenticated_client.get(path=url)
        assert response.status_code == 404

        # Old default is not affected
        assert getattr(default_address, f"is_{address_type}_default")

    @pytest.mark.parametrize("address_type", ["shipping", "billing"])
    def test_address_id_not_owned_by_user_throws_404(self, address_type, authenticated_client, user, other_user):
        """GIVEN an authenticated user

        WHEN the user tries to set an address owned by a different user
        as her new shipping or billing default address

        THEN the correct error is thrown and the old default is
        not affected."""
        default_address = Address.objects.create(
            user=user,
            is_shipping_default=True,
            is_billing_default=True,
            **OTHER_VALID_ADDRESS
        )

        # Create address not owned by user of interest
        non_owned_address = Address.objects.create(user=other_user, **VALID_ADDRESS_DATA)

        # Try to change default to non-owned address via API
        url = reverse("user:change_address_default") + f"?address-id={non_owned_address.id}&type={address_type}"
        response = authenticated_client.get(path=url)
        assert response.status_code == 404

        # Old default is not affected
        assert getattr(default_address, f"is_{address_type}_default")
