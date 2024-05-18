from enum import StrEnum


class ActionType(StrEnum):
    offer_connection = "offer.connection"
    offer_cancel = "offer.cancel"
    offer_success = "offer.success"
