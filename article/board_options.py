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

    def is_valid(self, options: dict):
        """Returns True if the complete set of internal board options
        is validated against the set of externally available options.

        Raises BoardOptionError otherwise.
        """
        for label, values in options.items():
            if not self._validate_option(label, values):
                raise BoardOptionError(f"The '{label}' option does not conform with externally available options.")
            return True
