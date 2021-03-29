import pytest

from django.urls import reverse

from .models import User


@pytest.mark.django_db
class TestUserRegistration:
    VALID_CREDENTIALS = {
        "email": "charly@gmail.com",
        "password1": "SuperStrongPassword",
        "password2": "SuperStrongPassword"
    }
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

    def test_register_user_with_valid_credentials(self, client):
        """GIVEN a set of valid credentials

        WHEN a user tries to register

        THEN registration is successful and the user is
        inserted into the database.
        """
        response = client.post(path="/auth/registration/", data=self.VALID_CREDENTIALS)

        assert response.status_code == 201
        assert "key" in response.json()
        assert User.objects.all().count() == 1

    @pytest.mark.parametrize(
        "credentials, expected_response_key, expected_response_message",
        [
            pytest.param(
                CREDENTIALS_INVALID_EMAIL,
                "email",
                "Enter a valid email address.",
                id="invalid_email"
            ),
            pytest.param(
                CREDENTIALS_SHORT_PASSWORD,
                "password1",
                "This password is too short. It must contain at least 8 characters.",
                id="short_password"
            ),
            pytest.param(
                CREDENTIALS_PASSWORD_MISMATCH,
                "non_field_errors",
                "The two password fields didn't match.",
                id="password_mismatch"
            )
        ]
    )
    def test_reject_register_user_with_invalid_credentials(
            self,
            client,
            credentials,
            expected_response_key,
            expected_response_message
    ):
        """GIVEN a set of invalid credentials

        WHEN a user tries to register

        THEN registration is rejected and an appropriate error
        message is returned in the HttpResponse.
        """
        response = client.post(path="/auth/registration/", data=credentials)

        assert response.status_code == 400

        try:
            actual_message = response.json()[expected_response_key]
        except KeyError:
            pytest.fail("Did not receive expected response.")
        else:
            assert actual_message[0] == expected_response_message

        # No user was inserted into the database.
        assert not User.objects.all().exists()


@pytest.mark.django_db
class TestUserDetails:
    """Test collection for retrieving user details."""
    def test_user_gets_their_details(self, authenticated_client, user):
        response = authenticated_client.get(path=reverse("user:user_details"))
        assert response.status_code == 200

        expected_response = {
            'email': user.email,
            'id': user.pk,
            'profile': {
                'default_shipping_address': user.profile.default_shipping_address,
                'default_billing_address': user.profile.default_billing_address
            }
        }
        assert response.json() == expected_response

    def test_unauthenticated_user_does_not_get_user_details(self, client):
        response = client.get(path=reverse("user:user_details"))
        assert response.status_code == 403

        expected_response = {'detail': 'Authentication credentials were not provided.'}

        assert response.json() == expected_response
