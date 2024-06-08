"""Call offers action types module."""

from enum import StrEnum


class ActionType(StrEnum):
    """Call offers action types."""

    offer_connection = "offer.connection"
    offer_cancel = "offer.cancel"
    offer_success = "offer.success"
