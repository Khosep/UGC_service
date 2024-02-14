"""Общие настройки всего проекта."""

import os

from config.config_django import settings_django
from split_settings.tools import include


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# DATABASE
include("components/database.py")

# TEMPLATES
include("components/templates.py")

# INSTALLED_APPS
include("components/installed_apps.py")

# LOGGING
include("components/logging.py")

# DJANGO_REST_FRAMEWORK
include("components/restframework.py")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = settings_django.django_secret_key

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = settings_django.django_debug

ALLOWED_HOSTS = settings_django.django_allowed_hosts

AUTH_USER_MODEL = "users.User"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"


# Password validation

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

LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")


# Media files

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Corsheaders settings

CORS_ALLOWED_ORIGINS = [
    f"http://{host}:{settings_django.django_swagger_port}"
    for host in settings_django.django_allowed_hosts
]


LOCALE_PATHS = ["movies/locale"]

if DEBUG:

    def show_toolbar(request):
        return True

    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": show_toolbar,
    }

    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")

AUTHENTICATION_BACKENDS = [
    "users.auth.CustomBackend",
    # 'django.contrib.auth.backends.ModelBackend',
]
