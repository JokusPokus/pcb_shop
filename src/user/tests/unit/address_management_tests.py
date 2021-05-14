import pytest

from django.core.exceptions import ObjectDoesNotExist

from user.address_management import set_new_default, disable_old_default
from user.address_management import Address

from user.tests import VALID_ADDRESS_DATA


pytestmark = pytest.mark.unit


@pytest.mark.django_db
@pytest.mark.parametrize("default_type", ["shipping", "billing"])
class TestSetNewDefault:
    def test_new_default_is_set(self, user, default_type):
        # GIVEN
        address = Address.objects.create(
            user=user,
            is_shipping_default=False,
            is_billing_default=False,
            **VALID_ADDRESS_DATA
        )

        # WHEN
        set_new_default(_type=default_type, _user=user, _id=address.id)

        # THEN
        address.refresh_from_db()
        assert getattr(address, f"is_{default_type}_default")

    def test_set_existing_default_anew_has_no_effect(self, user, default_type):
        # GIVEN
        address = Address.objects.create(
            user=user,
            is_shipping_default=True,
            is_billing_default=True,
            **VALID_ADDRESS_DATA
        )

        # WHEN
        set_new_default(_type=default_type, _user=user, _id=address.id)

        # THEN
        address.refresh_from_db()
        assert getattr(address, f"is_{default_type}_default")

    def test_cannot_set_non_existing_address_as_default(self, user, default_type):
        # GIVEN
        NON_EXISTING_ADDRESS_ID = 9999
        assert not Address.objects.filter(id=NON_EXISTING_ADDRESS_ID).exists()

        # WHEN/THEN
        with pytest.raises(ObjectDoesNotExist):
            set_new_default(_type=default_type, _user=user, _id=NON_EXISTING_ADDRESS_ID)


@pytest.mark.django_db
@pytest.mark.parametrize("default_type", ["shipping", "billing"])
class TestDisableOldDefault:
    def test_old_default_is_disabled(self, user, default_type):
        # GIVEN
        address = Address.objects.create(
            user=user,
            is_shipping_default=True,
            is_billing_default=True,
            **VALID_ADDRESS_DATA
        )

        # WHEN
        disable_old_default(_type=default_type, _user=user)

        # THEN
        address.refresh_from_db()
        assert not getattr(address, f"is_{default_type}_default")

    def test_disable_default_without_existing_address_does_not_throw_error(self, user, default_type):
        # GIVEN
        assert user.addresses.count() == 0

        # WHEN/THEN
        try:
            disable_old_default(_type=default_type, _user=user)
        except Exception as err:
            pytest.fail("Disabling default should not throw error, but threw:", err)
