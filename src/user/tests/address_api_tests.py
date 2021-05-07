import pytest

from . import VALID_ADDRESS, OTHER_VALID_ADDRESS, INVALID_ADDRESS_FIELDS

from user.address_management import Address


@pytest.mark.django_db
class TestAddressCreationSuccess:
    def test_correct_http_response(self, client):
        """GIVEN valid address and an authenticated user

        WHEN that user tries to save the address

        THEN a 201 status code and the correct address data
        with default settings set to false is returned.
        """
        response = client.post(path=reverse("address_list"), data=VALID_ADDRESS)
        assert response.status_code == 201

        response_body = response.json()
        assert response_body["is_shipping_default"] is False
        assert response_body["is_billing_default"] is False

    def test_address_inserted_into_db(self, client, user):
        """GIVEN valid address data and an authenticated user

        WHEN that user tries to save the address

        THEN the address is inserted into the database
        and linked to the user, with defaults set to false.
        """
        response = client.post(path=reverse("address_list"), data=VALID_ADDRESS)
        address_id = response.json()["id"]
        assert user.addresses.filter(id=address_id, **VALID_ADDRESS).exists()

        address = Address.objects.get(id=address_id)
        assert not address.is_shipping_default
        assert not address.is_billing_default


@pytest.mark.django_db
class TestAddressCreationFailure:
    def test_correct_http_response_for_anonymous_user(self, create_address):
        """GIVEN valid address data and an anonymous user

        WHEN that user tries to create the address

        THEN a 403 status code and a rejection message is returned.
        """
        response = create_address(VALID_ADDRESS, anonymous=True)
        assert response.status_code == 403

        response_body = response.json()
        expected_response_body = {
            "detail": "Authentication credentials were not provided."
        }
        assert response_body == expected_response_body

    def test_address_not_created_for_anonymous_user(self, create_address):
        """GIVEN valid address data and an anonymous user

        WHEN that user tries to create the address

        THEN the address is not inserted into the database.
        """
        create_address(VALID_ADDRESS, anonymous=True)
        assert not Address.objects.filter(**VALID_ADDRESS).exists()

    @pytest.mark.parametrize("missing_attribute", [attribute for attribute in VALID_ADDRESS])
    def test_correct_http_response_to_incomplete_address(self, missing_attribute, create_address):
        """GIVEN incomplete address data and an authenticated user

        WHEN that user tries to create the address

        THEN a 400 status code and the correct error message are returned.
        """
        address_data = VALID_ADDRESS.copy()
        del address_data[missing_attribute]

        response = create_address(address_data)

        assert response.status_code == 400

        response_body = response.json()
        expected_response_body = {
            missing_attribute: [
                "This field is required."
            ]
        }
        assert response_body == expected_response_body

    @pytest.mark.parametrize("missing_attribute", [attribute for attribute in VALID_ADDRESS])
    def test_incomplete_address_not_inserted_into_db(self, missing_attribute, create_address):
        """GIVEN incomplete address data and an authenticated user

        WHEN that user tries to create the address

        THEN the address is not inserted into the database.
        """
        address_data = VALID_ADDRESS.copy()
        del address_data[missing_attribute]
        create_address(address_data)
        assert not Address.objects.filter(**address_data).exists()

    @pytest.mark.parametrize("invalid_fields", INVALID_ADDRESS_FIELDS)
    def test_invalid_address_data_throws_error(self, invalid_fields, create_address):
        """GIVEN an authenticated user

        WHEN that user tries to create an address with (partially) invalid data

        THEN the correct Http error is returned.
        """
        invalid_address = VALID_ADDRESS.copy()
        invalid_address.update(invalid_fields)
        response = create_address(invalid_address)

        assert response.status_code == 400


@pytest.mark.django_db
class TestAddressListSuccess:
    pass


@pytest.mark.django_db
class TestAddressListFailure:
    pass


@pytest.mark.django_db
class TestAddressUpdateSuccess:
    def test_correct_http_response_upon_success(self, create_address, update_address):
        """GIVEN an authenticated user with an existing address

        WHEN the user updates a part of that address

        THEN the correct Http response is returned.
        """
        create_response = create_address()
        address_id = create_response.json()["id"]

        update_response = update_address(address_id, zip_code="12345")
        assert update_response.status_code == 200

    def test_address_is_updated_in_db(self, create_address, update_address, user):
        """GIVEN an authenticated user with an existing address

        WHEN the user updates a part of that address

        THEN the address is correctly updated in the database.
        """
        response = create_address()
        address_id = response.json()["id"]

        UPDATED_ZIP_CODE = "12345"
        update_address(address_id, zip_code=UPDATED_ZIP_CODE)
        assert user.addresses.get(id=address_id).zip_code == UPDATED_ZIP_CODE


@pytest.mark.django_db
class TestAddressUpdateFailure:
    def test_updating_non_existing_address_throws_404(self, update_address):
        """GIVEN an authenticated user

        WHEN the user tries to update a non-existing address

        THEN the correct Http error code is returned.
        """
        ADDRESS_ID = 9999  # does not exist
        response = update_address(ADDRESS_ID, street="Beispielstraße")
        assert response.status_code == 404

    @pytest.mark.parametrize("update_dict", INVALID_ADDRESS_FIELDS)
    def test_updating_address_with_invalid_data_throws_error(self, update_dict, create_address, update_address):
        """GIVEN an authenticated user

        WHEN the user tries to update an existing address with invalid data

        THEN the correct Http error code is returned.
        """
        create_response = create_address()
        address_id = create_response.json()["id"]

        update_response = update_address(address_id, **update_dict)
        assert update_response.status_code == 400

    def test_anonymous_user_cannot_update_address(self, create_address, update_address, client):
        """GIVEN an anonymous user

        WHEN the user tries to update an existing address

        THEN permission is denied and the correct Http error code is returned.
        """
        create_response = create_address()
        address_id = create_response.json()["id"]

        update_response = update_address(address_id, anonymous=True, zip_code="12345")
        assert update_response.status_code == 403


@pytest.mark.django_db
class TestAddressDeletionSuccess:
    def test_correct_http_response_upon_deletion(self, create_address, delete_address):
        """GIVEN an authenticated user with an existing address

        WHEN the user deletes that address

        THEN the correct Http response is returned.
        """
        create_response = create_address()
        address_id = create_response.json()["id"]

        delete_response = delete_address(address_id)
        assert delete_response.status_code == 204

    def test_address_is_deleted_from_db(self, create_address, delete_address, user):
        """GIVEN an authenticated user with an existing address

        WHEN the user deletes that address via the API

        THEN the address is deleted in the database.
        """
        response = create_address()
        address_id = response.json()["id"]

        delete_address(address_id)
        assert not user.addresses.filter(id=address_id).exists()


@pytest.mark.django_db
class TestAddressDeletionFailure:
    def test_anonymous_user_cannot_delete_address(self, create_address, delete_address, client):
        """GIVEN an anonymous user

        WHEN the user tries to delete an existing address

        THEN permission is denied and the correct Http error code is returned.
        """
        create_response = create_address()
        address_id = create_response.json()["id"]

        delete_response = delete_address(address_id, anonymous=True)
        assert delete_response.status_code == 403

    def test_updating_non_existing_address_throws_404(self, delete_address):
        """GIVEN an authenticated user

        WHEN the user tries to delete a non-existing address

        THEN the correct Http error code is returned.
        """
        NON_EXISTING_ADDRESS_ID = 9999
        response = delete_address(NON_EXISTING_ADDRESS_ID)
        assert response.status_code == 404


@pytest.mark.django_db
class TestAddressDefaultChangeSuccess:
    @pytest.mark.parametrize("address_type", ["shipping", "billing"])
    def test_correct_http_response(self, address_type, create_address, set_as_default):
        """GIVEN an authenticated user with an existing address

        WHEN the user sets that address as the new shipping or billing
        default address

        THEN she receives a 200 Http response with a success message."""
        create_response = create_address()
        address_id = create_response.json()["id"]

        response = set_as_default(address_type, address_id)
        assert response.status_code == 200

        response_body = response.json()
        assert response_body.get("Success") == f"Default {address_type} address changed successfully"

    @pytest.mark.parametrize("address_type", ["shipping", "billing"])
    def test_default_change_removes_old_default(self, address_type, create_and_set_as_default, user):
        """GIVEN an authenticated user with an existing default
        shipping or billing address

        WHEN the user sets a new shipping or billing default address

        THEN the default status of the old default address is removed
        in the database."""
        create_and_set_as_default(address_type, VALID_ADDRESS)
        create_and_set_as_default(address_type, OTHER_VALID_ADDRESS)

        old_default = user.addresses.get(**VALID_ADDRESS)
        assert not getattr(old_default, f"is_{address_type}_default")

    @pytest.mark.parametrize("address_type", ["shipping", "billing"])
    def test_default_change_adds_new_default(self, address_type, create_and_set_as_default, user):
        """GIVEN an authenticated user with an existing default
        shipping or billing address

        WHEN the user sets a new shipping or billing default address

        THEN the default status of the new default address is set
        in the database."""
        create_and_set_as_default(address_type, VALID_ADDRESS)
        create_and_set_as_default(address_type, OTHER_VALID_ADDRESS)

        new_default = user.addresses.get(**OTHER_VALID_ADDRESS)
        assert getattr(new_default, f"is_{address_type}_default")


@pytest.mark.django_db
class TestAddressDefaultChangeFailure:
    @pytest.mark.parametrize("address_type", ["shipping", "billing"])
    def test_non_existing_address_as_default_throws_404(self, address_type, set_as_default):
        """GIVEN an authenticated user

        WHEN the user tries to set an address that does not exist
        as her new shipping or billing default address

        THEN the correct error is thrown."""
        ADDRESS_ID = 9999  # does not exist
        response = set_as_default(address_type, ADDRESS_ID)
        assert response.status_code == 404

        response_body = response.json()
        assert response_body.get("Error") == "Address does not exist for this user."

    @pytest.mark.parametrize("address_type", ["shipping", "billing"])
    def test_address_id_not_owned_by_user_throws_404(
            self,
            address_type,
            client,
            other_user,
            create_address,
            set_as_default
    ):
        """GIVEN an authenticated user

        WHEN the user tries to set an address owned by a different user
        as her new shipping or billing default address

        THEN the correct error is thrown."""
        # First user creates address
        create_response = create_address(VALID_ADDRESS)
        address_id = create_response.json()["id"]

        # Different user tries to set that address as default
        client.logout()
        client.force_login(other_user)

        response = set_as_default(address_type, address_id)
        assert response.status_code == 404

    @pytest.mark.parametrize("address_type", ["shipping", "billing"])
    def test_bad_address_id_does_not_affect_current_default(
            self,
            address_type,
            create_and_set_as_default,
            set_as_default,
            user
    ):
        """GIVEN an authenticated user

        WHEN the user tries to set an address that he does not own
        or that does not exist as her new shipping or billing default address

        THEN this does not affect the current default address."""
        create_and_set_as_default(address_type, VALID_ADDRESS)

        # Try to change default to non existing address
        ADDRESS_ID = 9999
        set_as_default(address_type, ADDRESS_ID)

        # First address should still be the default
        expected_default_address = user.addresses.get(**VALID_ADDRESS)
        assert getattr(expected_default_address, f"is_{address_type}_default")
