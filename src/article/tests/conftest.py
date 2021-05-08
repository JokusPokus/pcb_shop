import pytest


@pytest.fixture
def choice_attribute():
    return {
        "choices": [1, 2, 3]
    }


@pytest.fixture
def range_attribute():
    return {
        "range": {
            "min": 10,
            "max": 100,
        }
    }
