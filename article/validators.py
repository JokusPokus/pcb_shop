from typing import Optional
from django.core.exceptions import ValidationError
from django.apps import apps


class BoardOptionValidator:
    """Validates a set of internally offered board options
    against a set of externally available options.
    """
    def __init__(self, shop: Optional[str] = None):
        if shop is None:
            ExternalShop = apps.get_model('article', 'ExternalShop')
            shop = ExternalShop.objects.get(name="JLCPCB")
        self.shop = shop
        self.external_options = self._get_external_options()

    def _get_external_options(self):
        """Returns the most up-to-date version of the board options
        offered by self.shop.
        """
        return self.shop.externalboardoptions_set.first().attribute_options

    @staticmethod
    def _contains_choices(option_values):
        return "choices" in option_values

    @staticmethod
    def _contains_range(option_values):
        return "range" in option_values

    @staticmethod
    def _validate_choices(internal_values: dict, external_values: dict, label: str) -> None:
        if not set(internal_values["choices"]) <= set(external_values["choices"]):
            raise ValidationError(
                f"At least one internal option for '{label}' is not externally available.",
                code="choice"
            )
        return None

    @staticmethod
    def _validate_range(internal_values: dict, external_values: dict, label: str) -> None:
        if (
                internal_values["range"]["min"] < external_values["range"]["min"]
                or internal_values["range"]["max"] > external_values["range"]["max"]
        ):
            raise ValidationError(
                f"'{label}' span is not fully contained in externally available option span.",
                code="span"
            )
        return None

    def _validate_option(self, label: str, internal_values: dict) -> None:
        """Validates a single board option against externally available option."""
        external_values = self.external_options.get(label)

        if external_values is None:
            raise ValidationError(
                f"Externally available options do not contain '{label}'.",
                code="missing_label"
            )

        if self._contains_choices(internal_values) and self._contains_choices(external_values):
            self._validate_choices(internal_values, external_values, label)

        elif self._contains_range(internal_values) and self._contains_range(external_values):
            self._validate_range(internal_values, external_values, label)

        else:
            raise ValidationError(
                f"Board option types for internal and external '{label}' values do not match.",
                code="attribute_type"
            )
        return None

    def validate(self, options: dict) -> None:
        """Raises BoardOptionError if any of the internal board options
        is not valid against the set of externally available options.

        Returns None otherwise.
        """
        for label, values in options.items():
            self._validate_option(label, values)

        return None


def validate_external_consistency(options: dict) -> None:
    """Custom validator to validate internally offered board options against
    externally available board options.

    Raises ValidationError if internal options are not valid.
    """
    validator = BoardOptionValidator()
    validator.validate(options)
