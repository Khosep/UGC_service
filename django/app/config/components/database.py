"""Database."""

from config.config_django import settings_django

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": settings_django.django_postgres_db,
        "USER": settings_django.django_postgres_user,
        "PASSWORD": settings_django.django_postgres_password,
        "HOST": settings_django.django_postgres_host,
        "PORT": settings_django.django_postgres_port,
        "OPTIONS": {"options": "-c search_path=public,content"},
    },
}
