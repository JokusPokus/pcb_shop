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
