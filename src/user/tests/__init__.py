import pytest


VALID_ADDRESS = {
    "receiver_first_name": "Max",
    "receiver_last_name": "Mustermann",
    "street": "Musterstraße",
    "house_number": "99",
    "zip_code": "99999",
    "city": "Musterhause"
}

OTHER_VALID_ADDRESS = {
    "receiver_first_name": "Maxime",
    "receiver_last_name": "Musterfrau",
    "street": "Musterstraße",
    "house_number": "88",
    "zip_code": "88888",
    "city": "Musterheim"
}

INVALID_ADDRESS_FIELDS = [
    (pytest.param({"zip_code": "1234"}, id="Zip too short")),
    (pytest.param({"zip_code": "123456"}, id="Zip too long")),
    (pytest.param({"receiver_first_name": "a" * 100}, id="Name too long")),
    (pytest.param({"house_number": "1000000 c"}, id="House number too long"))
]
