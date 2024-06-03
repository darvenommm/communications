"""Register rest routes module."""

from rest_framework.routers import BaseRouter

from .subscriber import SubscriberViewSet

routes = (("subscribers", SubscriberViewSet),)


def register_rest_routes(router: BaseRouter) -> None:
    """Register rest routes.

    Args:
        router: The main rest router.
    """
    for prefix, view_set in routes:
        router.register(prefix, view_set)
