from rest_framework.routers import BaseRouter

from .view_sets import (
    SubscriberCallViewSet,
)

from .subscriber import SubscriberViewSet
from .operator import OperatorViewSet


routes = (
    ("operators", OperatorViewSet),
    ("subscribers", SubscriberViewSet),
    ("subscribers_calls", SubscriberCallViewSet),
)


def register_routes(router: BaseRouter) -> BaseRouter:
    for prefix, view_set in routes:
        router.register(prefix, view_set)

    return router
