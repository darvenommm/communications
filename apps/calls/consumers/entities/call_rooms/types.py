from enum import StrEnum


class ActionType(StrEnum):
    offer = "offer"
    answer = "answer"
    final = "final"
    candidate = "candidate"
    connected = "connected"
    close = "close"
