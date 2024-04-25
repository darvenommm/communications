from rest_framework.routers import BaseRouter

from .view_sets import UserViewSet


routes = (("users", UserViewSet),)


def register_routes(router: BaseRouter) -> BaseRouter:
    for prefix, view_set in routes:
        router.register(prefix, view_set)

    return router
