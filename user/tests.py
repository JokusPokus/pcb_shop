import pytest


@pytest.mark.django_db
def test_register_user_with_valid_credentials(client):
    """GIVEN a set of valid credentials
    WHEN a user tries to register
    THEN registration is successful.
    """
    VALID_CREDENTIALS = {
        "email": "charly@gmail.com",
        "password1": "SuperStrongPassword",
        "password2": "SuperStrongPassword"
    }
    response = client.post(path="/auth/registration/", data=VALID_CREDENTIALS)

    assert response.status_code == 201


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
@pytest.mark.django_db
def test_reject_register_user_with_invalid_credentials(
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
