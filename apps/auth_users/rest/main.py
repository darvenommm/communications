from rest_framework.routers import BaseRouter

from .user import UserViewSet


routes = (("users", UserViewSet),)


def register_rest_routes(router: BaseRouter) -> BaseRouter:
    for prefix, view_set in routes:
        router.register(prefix, view_set)

    return router
