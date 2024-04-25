from rest_framework.routers import BaseRouter

from .operator_view_set import OperatorViewSet


routes = (("operators", OperatorViewSet),)


def register_routes(router: BaseRouter) -> BaseRouter:
    for prefix, view_set in routes:
        router.register(prefix, view_set)

    return router
