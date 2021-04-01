import pytest

from django.urls import reverse

from user.models import User
from user.address_management import Address
from user.tests.conftest import VALID_ADDRESS


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
        response = create_address
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
        response = create_address
        address_id = response.json()["id"]
        assert user.addresses.filter(id=address_id, **VALID_ADDRESS).exists()


@pytest.mark.django_db
class TestAddressCreationFailure:
    def test_correct_http_response_for_anonymous_user(self, create_address_with_anonymous_user):
        """GIVEN valid address data and an anonymous user

        WHEN that user tries to create the address

        THEN a 403 status code and a rejection message is returned.
        """
        response = create_address_with_anonymous_user
        assert response.status_code == 403

        response_body = response.json()
        expected_response_body = {
            "detail": "Authentication credentials were not provided."
        }
        assert response_body == expected_response_body

    def test_address_not_created_for_anonymous_user(
            self,
            create_address_with_anonymous_user
    ):
        """GIVEN valid address data and an anonymous user

        WHEN that user tries to create the address

        THEN the address is not inserted into the database.
        """
        assert not Address.objects.filter(**VALID_ADDRESS).exists()

    def test_correct_http_response_to_incomplete_address(self, create_incomplete_address):
        """GIVEN incomplete address data and an authenticated user

        WHEN that user tries to create the address

        THEN a 400 status code and the correct error message are returned.
        """
        missing_attribute, _, response = create_incomplete_address
        assert response.status_code == 400

        response_body = response.json()
        expected_response_body = {
            missing_attribute: [
                "This field is required."
            ]
        }
        assert response_body == expected_response_body

    def test_incomplete_address_not_inserted_into_db(
            self,
            create_incomplete_address
    ):
        """GIVEN incomplete address data and an authenticated user

        WHEN that user tries to create the address

        THEN the address is not inserted into the database.
        """
        _, address_data, _ = create_incomplete_address
        assert not Address.objects.filter(**address_data).exists()


@pytest.mark.django_db
class TestAddressListSuccess:
    pass


@pytest.mark.django_db
class TestAddressListFailure:
    pass


@pytest.mark.django_db
class TestAddressUpdateSuccess:
    pass


@pytest.mark.django_db
class TestAddressUpdateFailure:
    pass


@pytest.mark.django_db
class TestAddressDeletionSuccess:
    pass


@pytest.mark.django_db
class TestAddressDeletionFailure:
    pass


@pytest.mark.django_db
class TestAddressDefaultChangeSuccess:
    pass


@pytest.mark.django_db
class TestAddressDefaultChangeFailure:
    pass