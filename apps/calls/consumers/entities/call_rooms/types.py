from enum import StrEnum


class ActionType(StrEnum):
    who = "who"
    offer_send = "offer.send"
    offer_get = "offer.get"
    answer_send = "answer.send"
    answer_get = "answer.get"
    candidate_send = "candidate.send"
    candidate_get = "candidate.get"


class WhoAmI(StrEnum):
    starter = "starter"
    answerer = "answerer"
