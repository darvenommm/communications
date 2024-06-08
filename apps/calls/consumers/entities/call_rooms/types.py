"""Call room action types module."""

from enum import StrEnum


class ActionType(StrEnum):
    """Call room action types."""

    offer = "offer"
    answer = "answer"
    final = "final"
    candidate = "candidate"
    connected = "connected"
    close = "close"
    time_limit = "time.limit"
