"""Registration of rest routes module."""

from rest_framework.routers import BaseRouter

from .operator import OperatorViewSet
from .subscriber_call import SubscriberCallViewSet

routes = (
    ("operators", OperatorViewSet),
    ("subscribers_calls", SubscriberCallViewSet),
)


def register_rest_routes(router: BaseRouter) -> None:
    """Register rest routes.

    Args:
        router: The given router.
    """
    for prefix, view_set in routes:
        router.register(prefix, view_set)
