from typing import Optional
from article.models import ExternalShop


class BoardOptionError(Exception):
    """Raised when internal board option does not confirm with externally available one."""
    pass


class BoardOptionValidator:
    """Validates a set of internally offered board options
    against a set of externally available options.
    """
    def __init__(self, shop: Optional[str] = None):
        if shop is None:
            shop = ExternalShop.objects.get(name="JLCPCB")
        self.shop = shop
        self.external_options = self._get_external_options()

    def _get_external_options(self):
        """Returns the most up-to-date version of the board options
        offered by self.shop.
        """
        return self.shop.externalboardoptions_set.first()

    def _validate_option(self, label: str, internal_values: dict) -> None:
        """Validates a single board option against externally available option."""
        external_values = self.external_options.get(label)

        if external_values is None:
            raise BoardOptionError(f"Externally available options do not contain '{label}'.")

        if "choices" in internal_values and "choices" in external_values:
            if not set(internal_values) <= set(external_values):
                raise BoardOptionError(f"At least one internal option for '{label}' is not externally available.")

        elif "range" in internal_values and "range" in external_values:
            if (
                    internal_values["range"]["min"] < external_values["range"]["min"]
                    or internal_values["range"]["max"] > external_values["range"]["max"]
            ):
                raise BoardOptionError(f"'{label}' span is not fully contained in externally available option span.")

        else:
            raise BoardOptionError(f"Board option types for internal and external '{label}' values do not match.")

        return None

    def validate(self, options: dict) -> bool:
        """Raises BoardOptionError if any of the internal board options
        is not valid against the set of externally available options.

        Returns None otherwise.
        """
        for label, values in options.items():
            self._validate_option(label, values)

        return None
