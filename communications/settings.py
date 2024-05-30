"""
Django settings for communications project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from os import getenv
from pathlib import Path
import sys

from django.utils.translation import gettext_lazy as _

from dotenv import load_dotenv

load_dotenv()

# add the apps directory to python paths
apps_path = Path(__file__).parent.parent.resolve() / "apps"
sys.path.append(apps_path.absolute().as_posix())


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-)+&c!1l#ftfs@j=8dqe1@fy^r1r-h0=qdc9!g))u5s(*ai)+0b"

# SECURITY WARNING: don't run with debug turned on in production!
IS_PRODUCTION = getenv("IS_PRODUCTION", False)
IS_DEVELOPMENT = not IS_PRODUCTION

DEBUG = IS_DEVELOPMENT


ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "daphne",
    "subscribers",
    "calls",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "communications.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


REDIS_PORT = int(getenv("REDIS_PORT", 6379))

WSGI_APPLICATION = "communications.wsgi.application"
ASGI_APPLICATION = "communications.asgi.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", REDIS_PORT)],
        },
    },
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://127.0.0.1:{REDIS_PORT}/",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
        },
    }
}

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DB_PASSWORD = getenv("DB_PASSWORD")

if not DB_PASSWORD:
    raise ValueError("Not defined DB_PASSWORD in .env file!")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": getenv("DB_NAME", "communications"),
        "USER": getenv("DB_USER", "postgres"),
        "PASSWORD": DB_PASSWORD,
        "HOST": getenv("DB_HOST", "127.0.0.1"),
        "PORT": int(5432 if IS_PRODUCTION else getenv("DB_PORT", 5432)),
        "OPTIONS": {
            "options": "-c search_path=communications,public",
        },
    },
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

LANGUAGES = (
    ("en", _("English")),
    ("ru", _("Russian")),
)

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "subscribers.Subscriber"


REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
}

REST_FRAMEWORK_API_PATH = "api/"

if IS_DEVELOPMENT:
    REST_FRAMEWORK.get("DEFAULT_RENDERER_CLASSES", []).append(
        "rest_framework.renderers.BrowsableAPIRenderer",
    )

LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"
LOGIN_URL = "auth:log_in"
