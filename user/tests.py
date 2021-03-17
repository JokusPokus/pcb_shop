import pytest

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


@pytest.mark.parametrize(
    "credentials, expected_status_code",
    [
        (VALID_CREDENTIALS, 201),
        (CREDENTIALS_INVALID_EMAIL, 400),
        (CREDENTIALS_SHORT_PASSWORD, 400),
        (CREDENTIALS_PASSWORD_MISMATCH, 400)
    ]
)
@pytest.mark.django_db
def test_register_user(client, credentials, expected_status_code):
    response = client.post("/auth/registration/", credentials)
    assert response.status_code == expected_status_code




