from typing import Optional
from article.models import ExternalShop


class BoardOptionValidator:
    """Validates a set of internally offered board options
    against a set of externally available options.
    """
    def __init__(self, shop: Optional[str] = None):
        if shop is None:
            pass
        pass
