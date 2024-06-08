"""Subscribers websocket action types module."""

from enum import StrEnum


class ActionType(StrEnum):
    """Subscribers websocket action types."""

    subscribers_online = "subscribers.online"
    subscriber_invite = "subscriber.invite"
    subscriber_discard = "subscriber.discard"
