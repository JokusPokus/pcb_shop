from typing import Optional, Union
from django.core.exceptions import ValidationError
from django.apps import apps


class AttributeValidator:
    """Validates a specific attribute configuration against the
    currently offered board options.
    """
    def __init__(self):
        self.offered_options: dict = self._get_current_options()

    @staticmethod
    def _get_current_options() -> dict:
        """Returns the most up-to-date version of the internally offered board options."""
        OfferedBoardOptions = apps.get_model('article', 'OfferedBoardOptions')
        return OfferedBoardOptions.objects.latest("created").attribute_options

    @staticmethod
    def _validate_choice(value: Union[str, int, float], offered_values: list, label: str) -> None:
        if value not in offered_values:
            raise ValidationError(
                f"Choice '{value}' is not available for attribute '{label}'.",
                code="out_of_choices"
            )

    @staticmethod
    def _validate_range(value: Union[str, int, float], offered_values: dict, label: str) -> None:
        if not offered_values["min"] <= value <= offered_values["max"]:
            raise ValidationError(
                f"'{value}' is not in available range for attribute '{label}'.",
                code="out_of_range"
            )

    def _validate_attribute(self, label: str, value: Union[str, int, float]) -> None:
        offered_attribute_values = self.offered_options.get(label)

        if offered_attribute_values is None:
            raise ValidationError(f"The '{label}' option is currently not offered.", code="option_not_offered")

        if "choices" in offered_attribute_values:
            self._validate_choice(value, offered_attribute_values["choices"], label)

        elif "range" in offered_attribute_values:
            self._validate_range(value, offered_attribute_values["range"], label)

        else:
            raise ValidationError(f"""Currently offered board options for '{label}' are malformed. 
No choices or range attribute is present.""")

    def validate(self, attributes: dict) -> None:
        """Raises ValidationError if any of the board attributes
        is not valid against the currently offered options.

        Returns None otherwise.
        """
        for label, value in attributes.items():
            self._validate_attribute(label, value)

        return None


class BoardOptionValidator:
    """Validates a set of internally offered board options
    against a set of externally available options.
    """
    def __init__(self, shop: Optional[str] = None):
        if shop is None:
            ExternalShop = apps.get_model('article', 'ExternalShop')
            shop = ExternalShop.objects.get(name="Example PCB Shop")
        self.shop = shop
        self.external_options = self._get_external_options()

    def _get_external_options(self):
        """Returns the most up-to-date version of the board options
        offered by self.shop.
        """
        return self.shop.externalboardoptions_set.latest("created").attribute_options

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
        """Raises ValidationError if any of the internal board options
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
