import pytest

from django.urls import reverse

from user.models import User
from user.address_management import Address
from user.tests.conftest import VALID_ADDRESS, OTHER_VALID_ADDRESS, INVALID_ADDRESS_FIELDS


@pytest.mark.django_db
class TestUserRegistrationSuccess:
    """GIVEN a set of valid credentials

    WHEN a client tries to register a user

    THEN a token key is returned and the user is
    inserted into the database.
    """
    @pytest.fixture
    def register_with_valid_credentials(self, db, client, valid_credentials):
        response = client.post(path="/auth/registration/", data=valid_credentials)
        return response

    def test_201_status_and_token_key_returned(self, register_with_valid_credentials):
        response = register_with_valid_credentials
        assert response.status_code == 201

        response_body = response.json()
        assert "key" in response_body

    def test_user_inserted_in_db(self, register_with_valid_credentials, valid_credentials):
        assert User.objects.filter(email=valid_credentials["email"]).exists()


@pytest.mark.django_db
class TestUserRegistrationFailure:
    """Test collection for intentional failures of user registration."""
    CREDENTIALS_INVALID_EMAIL = {
        "email": "charly@gmail",
        "password1": "SuperStrongPassword",
        "password2": "SuperStrongPassword"
    }
    CREDENTIALS_SHORT_PASSWORD = {
        "email": "charly@gmail.com",
        "password1": "short",
        "password2": "short"
    }
    CREDENTIALS_PASSWORD_MISMATCH = {
        "email": "charly@gmail.com",
        "password1": "SuperStrongPassword",
        "password2": "DifferentPassword"
    }

    # Set up test cases with expected responses
    # to pass to test function as parameters
    invalid_credentials_test_cases = [
        pytest.param(
            CREDENTIALS_INVALID_EMAIL,
            "email",
            ["Enter a valid email address."],
            id="invalid_email"
        ),
        pytest.param(
            CREDENTIALS_SHORT_PASSWORD,
            "password1",
            ["This password is too short. It must contain at least 8 characters."],
            id="short_password"
        ),
        pytest.param(
            CREDENTIALS_PASSWORD_MISMATCH,
            "non_field_errors",
            ["The two password fields didn't match."],
            id="password_mismatch"
        )
    ]

    @pytest.mark.parametrize(
        "credentials, expected_response_key, expected_response_message",
        invalid_credentials_test_cases
    )
    def test_registration_with_invalid_credentials(
            self,
            client,
            credentials,
            expected_response_key,
            expected_response_message
    ):
        """GIVEN a set of invalid credentials

        WHEN a client tries to register a user

        THEN registration is rejected and the correct error
        message is returned in the HttpResponse.
        """
        response = client.post(path="/auth/registration/", data=credentials)

        assert response.status_code == 400

        response_body = response.json()
        assert expected_response_key in response_body

        actual_message = response_body[expected_response_key]
        assert actual_message == expected_response_message

    def test_registration_with_taken_email(self, client, valid_credentials):
        """GIVEN an anonymous user

        WHEN they try to register with an email that is already taken
        but otherwise valid credentials

        THEN registration is rejected and the correct error
        message is returned in the HttpResponse.
        """
        # User is registered
        client.post(path="/auth/registration/", data=valid_credentials)
        assert User.objects.filter(email=valid_credentials["email"]).exists()

        # Second user registration with the same credentials is rejected
        response = client.post(path="/auth/registration/", data=valid_credentials)
        assert response.status_code == 400

        response_body = response.json()
        expected_response_body = {
            'email': ['A user is already registered with this e-mail address.']
        }
        assert response_body == expected_response_body


@pytest.mark.django_db
class TestUserDetailsSuccess:
    """GIVEN an authenticated user

    WHEN that user tries to retrieve their user details

    THEN a correct and complete object with user details
    is returned."""
    def test_user_retrieves_personal_details(self, authenticated_client, user):
        response = authenticated_client.get(path=reverse("user:user_details"))
        assert response.status_code == 200

        expected_response_body = {
            'email': user.email,
            'id': user.pk,
            'profile': {}
        }
        response_body = response.json()
        assert response_body == expected_response_body


@pytest.mark.django_db
class TestUserDetailsFailure:
    def test_unauthenticated_user_does_not_retrieve_user_details(self, client):
        """GIVEN an unauthenticated user

        WHEN that user tries to retrieve user details

        THEN an error code and the correct error message are
        returned."""
        response = client.get(path=reverse("user:user_details"))
        assert response.status_code == 403

        response_body = response.json()
        expected_response_body = {'detail': 'Authentication credentials were not provided.'}
        assert response_body == expected_response_body


@pytest.mark.django_db
class TestAddressCreationSuccess:
    def test_correct_http_response(self, create_address):
        """GIVEN valid address and an authenticated user

        WHEN that user tries to save the address

        THEN a 201 status code and the correct address data
        with default settings set to false is returned.
        """
        response = create_address()
        assert response.status_code == 201

        response_body = response.json()
        expected_response_data = VALID_ADDRESS.copy()
        expected_response_data.update({
            "is_shipping_default": False,
            "is_billing_default": False
        })
        # Expected response data is contained in response_body
        assert expected_response_data.items() <= response_body.items()

    def test_address_inserted_into_db(self, create_address, user):
        """GIVEN valid address data and an authenticated user

        WHEN that user tries to save the address

        THEN the address is inserted into the database.
        """
        response = create_address()
        address_id = response.json()["id"]
        assert user.addresses.filter(id=address_id, **VALID_ADDRESS).exists()

    def test_address_is_not_set_to_default(self, create_address, user):
        """GIVEN valid address data and an authenticated user

        WHEN that address is saved into the database

        THEN the address is not set to be a shipping or billing
        default.
        """
        response = create_address()
        address_id = response.json()["id"]
        new_address = user.addresses.get(id=address_id)
        assert not new_address.is_shipping_default
        assert not new_address.is_billing_default


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

        THEN the correct Http response is returned."""
        create_response = create_address()
        address_id = create_response.json()["id"]

        update_response = update_address(address_id, zip_code="12345")
        assert update_response.status_code == 200

    def test_address_is_updated_in_db(self, create_address, update_address, user):
        """GIVEN an authenticated user with an existing address

        WHEN the user updates a part of that address

        THEN the address is correctly updated in the database."""
        response = create_address()
        address_id = response.json()["id"]

        UPDATED_ZIP_CODE = "12345"
        update_address(address_id, zip_code=UPDATED_ZIP_CODE)
        assert user.addresses.get(id=address_id).zip_code == UPDATED_ZIP_CODE


@pytest.mark.django_db
class TestAddressUpdateFailure:
    def test_updating_non_existing_address_throws_404(self, update_address):
        ADDRESS_ID = 9999  # does not exist
        response = update_address(ADDRESS_ID, street="Beispielstraße")
        assert response.status_code == 404

    @pytest.mark.parametrize("update_dict", INVALID_ADDRESS_FIELDS)
    def test_updating_address_with_invalid_data_throws_error(self, update_dict, create_address, update_address):
        create_response = create_address()
        address_id = create_response.json()["id"]

        update_response = update_address(address_id, **update_dict)
        assert update_response.status_code == 400


@pytest.mark.django_db
class TestAddressDeletionSuccess:
    pass


@pytest.mark.django_db
class TestAddressDeletionFailure:
    pass


@pytest.mark.django_db
class TestAddressDefaultChangeSuccess:
    def test_correct_http_response(self, create_address, set_as_default):
        """GIVEN an authenticated user with an existing address

        WHEN the user sets that address as the new shipping or billing
        default address

        THEN she receives a 200 Http response with a success message."""
        create_response = create_address()
        address_id = create_response.json()["id"]

        response = set_as_default(address_id)
        assert response.status_code == 200

        response_body = response.json()
        assert "address changed successfully" in response_body.get("Success")

    def test_default_change_removes_old_default(self, create_and_set_as_default, user):
        """GIVEN an authenticated user with an existing default
        shipping or billing address

        WHEN the user sets a new shipping or billing default address

        THEN the default status of the old default address is removed
        in the database."""
        create_and_set_as_default(VALID_ADDRESS)
        create_and_set_as_default(OTHER_VALID_ADDRESS)

        old_default = user.addresses.get(**VALID_ADDRESS)
        assert not old_default.is_shipping_default
        assert not old_default.is_billing_default

    def test_default_change_adds_new_default(self, create_and_set_as_default, user):
        """GIVEN an authenticated user with an existing default
        shipping or billing address

        WHEN the user sets a new shipping or billing default address

        THEN the default status of the new default address is set
        in the database."""
        create_and_set_as_default(VALID_ADDRESS)
        create_and_set_as_default(OTHER_VALID_ADDRESS)

        new_default = user.addresses.get(**OTHER_VALID_ADDRESS)
        assert new_default.is_shipping_default or new_default.is_billing_default


@pytest.mark.django_db
class TestAddressDefaultChangeFailure:
    def test_non_existing_address_as_default_throws_404(self, set_as_default):
        """GIVEN an authenticated user

        WHEN the user tries to set an address that does not exist
        as her new shipping or billing default address

        THEN the correct error is thrown."""
        ADDRESS_ID = 9999  # does not exist
        response = set_as_default(ADDRESS_ID)
        assert response.status_code == 404

        response_body = response.json()
        assert response_body.get("Error") == "Address does not exist for this user."

    def test_address_id_not_owned_by_user_throws_404(self, client, other_user, create_address, set_as_default):
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

        response = set_as_default(address_id)
        assert response.status_code == 404

    def test_bad_address_id_does_not_affect_current_default(
            self,
            create_and_set_as_default,
            authenticated_client,
            user
    ):
        """GIVEN an authenticated user

        WHEN the user tries to set an address that he does not own
        or that does not exist as her new shipping or billing default address

        THEN this does not affect the current default address."""
        create_and_set_as_default(VALID_ADDRESS)

        # Change default to non existing address
        ADDRESS_ID = 9999
        for address_type in ["billing", "shipping"]:
            path = reverse("user:change_address_default") + f"?address_id={ADDRESS_ID}&type={address_type}"
            authenticated_client.get(path=path)

        expected_default_address = user.addresses.get(**VALID_ADDRESS)
        assert expected_default_address.is_shipping_default or expected_default_address.is_billing_default
