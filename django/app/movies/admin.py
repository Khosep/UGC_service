"""Настройки админки Django."""
from django.contrib import admin

from movies.models import (
    FilmWork,
    Genre,
    GenreFilmWork,
    Person,
    PersonFilmWork,
)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Регистрация и настройка класса Genre."""

    list_display = ("name", "description", "created", "modified")
    list_filter = ("name",)
    search_fields = ("name", "description", "id")


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    """Регистрация и настройка класса Person."""

    list_display = ("full_name", "created", "modified")
    list_filter = ("full_name",)
    search_fields = ("full_name", "id")


class GenreFilmWorkInline(admin.TabularInline):
    """Инлайн для жанров в кинопроизведениях."""

    model = GenreFilmWork


class PersonFilmWorkInline(admin.TabularInline):
    """Инлайн для персон в кинопроизведениях."""

    model = PersonFilmWork
    raw_id_fields = ["person"]


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    """Регистрация и настройка класса FilmWork."""

    inlines = (GenreFilmWorkInline, PersonFilmWorkInline)
    list_display = (
        "title",
        "type",
        "creation_date",
        "rating",
        "created",
        "modified",
    )
    list_filter = ("type",)
    search_fields = ("title", "description", "id")
