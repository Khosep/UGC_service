"""Инициализация приложения movies."""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    """Базовые настройки приложения users."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
    verbose_name = _("users")

    def ready(self):
        pass
