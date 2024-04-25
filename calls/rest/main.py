from rest_framework.routers import BaseRouter

from .view_sets import (
    OperatorViewSet,
    SubscriberViewSet,
    SubscriberCallViewSet,
    OperatorSubscriberViewSet,
)


routes = (
    ("operators", OperatorViewSet),
    ("subscribers", SubscriberViewSet),
    ("subscribers_calls", SubscriberCallViewSet),
    ("operators_subscriber", OperatorSubscriberViewSet),
)


def register_routes(router: BaseRouter) -> BaseRouter:
    for prefix, view_set in routes:
        router.register(prefix, view_set)

    return router
