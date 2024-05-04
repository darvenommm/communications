from rest_framework.routers import BaseRouter

from .subscriber import SubscriberViewSet
from .operator import OperatorViewSet
from .subscriber_call import SubscriberCallViewSet


routes = (
    ("operators", OperatorViewSet),
    ("subscribers", SubscriberViewSet),
    ("subscribers_calls", SubscriberCallViewSet),
)


def register_rest_routes(router: BaseRouter) -> BaseRouter:
    for prefix, view_set in routes:
        router.register(prefix, view_set)

    return router
