import pytest

from django.urls import reverse

from user.models import User

from . import VALID_CREDENTIALS


@pytest.mark.django_db
class TestUserRegistrationSuccess:
    def test_registration_with_valid_credentials_is_successful(self, client):
        """GIVEN a set of valid credentials

        WHEN a client tries to register a user

        THEN a token key is returned and the user is
        inserted into the database.
        """
        response = client.post(path="/auth/registration/", data=VALID_CREDENTIALS)
        assert response.status_code == 201

        # Token key is returned
        response_body = response.json()
        assert "key" in response_body

        # User has been inserted into database
        assert User.objects.filter(email=VALID_CREDENTIALS["email"]).exists()


@pytest.mark.django_db
class TestUserRegistrationFailure:
    @pytest.mark.parametrize("invalid_fields", [
        (pytest.param({"email": "charly@gmail"}, id="Invalid email")),
        (pytest.param({"password1": "short", "password2": "short"}, id="Password too short")),
        (pytest.param({"password1": "StrongPassword", "password2": "AlsoAStrongPassword"}, id="Password mismatch"))
    ])
    def test_registration_with_invalid_credentials(self, invalid_fields, client):
        """GIVEN a set of invalid credentials

        WHEN a client tries to register a user

        THEN registration is rejected and the correct error
        message is returned in the HttpResponse.
        """
        invalid_credentials = {**VALID_CREDENTIALS, **invalid_fields}
        response = client.post(path="/auth/registration/", data=invalid_credentials)
        assert response.status_code == 400

        # User has not been inserted into database
        assert not User.objects.filter(email=invalid_credentials["email"]).exists()

    def test_registration_with_taken_email(self, client):
        """GIVEN an anonymous user

        WHEN they try to register with an email that is already taken
        but otherwise valid credentials

        THEN registration is rejected and the correct error
        message is returned in the HttpResponse.
        """
        # User is created
        client.post(path="/auth/registration/", data=VALID_CREDENTIALS)
        assert User.objects.filter(email=VALID_CREDENTIALS["email"]).exists()

        # Second user tries to register with same credentials
        response = client.post(path="/auth/registration/", data=VALID_CREDENTIALS)
        assert response.status_code == 400


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
            'id': user.pk
        }
        response_body = response.json()
        assert response_body == expected_response_body


@pytest.mark.django_db
class TestUserDetailsFailure:
    def test_anonymous_user_does_not_retrieve_user_details(self, client):
        """GIVEN an anonymous user

        WHEN that user tries to retrieve user details

        THEN an error code and the correct error message are
        returned."""
        response = client.get(path=reverse("user:user_details"))
        assert response.status_code == 403

        response_body = response.json()
        expected_response_body = {'detail': 'Authentication credentials were not provided.'}
        assert response_body == expected_response_body
