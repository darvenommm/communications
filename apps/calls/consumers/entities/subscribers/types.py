from enum import StrEnum


class ActionType(StrEnum):
    subscribers_online = "subscribers.online"
    subscriber_invite = "subscriber.invite"
    subscriber_discard = "subscriber.discard"
