"""Настройки админки Django."""
from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Регистрация и настройка класса User."""

    list_display = ("username", "email", "is_active", "is_admin")
    list_filter = ("username", "email")
    search_fields = ("username", "email", "id")
