import pytest


@pytest.fixture
def valid_credentials():
    return {
        "email": "charly@gmail.com",
        "password1": "SuperStrongPassword",
        "password2": "SuperStrongPassword"
    }
