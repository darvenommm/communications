"""
URL configuration for communications project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from auth_users.rest import register_rest_routes as auth_user_register
from calls.rest import register_rest_routes as calls_register


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
        path("", include("calls.urls", namespace="calls")),
        prefix_default_language=False,
    ),
]
