"""Project urls."""

from calls.rest import register_rest_routes as calls_register
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from subscribers.rest import register_rest_routes as auth_user_register

router = DefaultRouter()
registers = (auth_user_register, calls_register)

for register in registers:
    register(router)


urlpatterns = [
    path(settings.REST_FRAMEWORK_API_PATH, include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api-token-auth/", views.obtain_auth_token),
    *i18n_patterns(
        path("admin/", admin.site.urls),
        path("auth/", include("subscribers.urls", namespace="auth")),
        path("", include("calls.urls")),
        prefix_default_language=False,
    ),
]
