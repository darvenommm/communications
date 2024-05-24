from enum import StrEnum


class ActionType(StrEnum):
    offer_create = "offer.create"
    offer_send = "offer.send"
    answer_create = "answer.create"
    answer_send = "answer.send"
    answer_get = "answer.get"
