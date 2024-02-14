"""Модели приложения movies."""
import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from movies.constants import CHARFIELD_MAX_LENGTH


class CreatedMixin(models.Model):
    """Абстрактная модель для поля created."""

    created = models.DateTimeField(_("created"), auto_now_add=True)

    class Meta:
        abstract = True


class TimeStampedMixin(CreatedMixin):
    """Абстрактная модель для полей created и modifed."""

    modified = models.DateTimeField(_("modified"), auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    """Абстрактная модель для поля id."""

    id = models.UUIDField(
        "ID",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    """Модель жанров."""

    name = models.CharField(
        _("name"),
        max_length=CHARFIELD_MAX_LENGTH,
        unique=True,
    )
    description = models.TextField(_("description"), blank=True, null=True)

    class Meta:
        db_table = "genre"
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")

    def __str__(self):
        return self.name


class Person(UUIDMixin, TimeStampedMixin):
    """Модель персон."""

    full_name = models.CharField(
        _("full_name"),
        max_length=CHARFIELD_MAX_LENGTH,
        unique=True,
    )

    class Meta:
        db_table = "person"
        verbose_name = _("Person")
        verbose_name_plural = _("Persons")

    def __str__(self):
        return self.full_name


class FilmWork(UUIDMixin, TimeStampedMixin):
    """Модель кинопроизведений."""

    class Type(models.TextChoices):
        """Класс вариантов выбора типов жанров."""

        movie = "movie"
        tv_show = "tv_show"

    title = models.CharField(_("title"), max_length=CHARFIELD_MAX_LENGTH)
    description = models.TextField(_("description"), blank=True, null=True)
    creation_date = models.DateField(_("creation_date"), blank=True, null=True)
    rating = models.FloatField(
        _("rating"),
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    type = models.TextField(
        _("type"), choices=Type.choices, blank=True, null=True
    )
    genres = models.ManyToManyField(
        Genre,
        through="GenreFilmwork",
        verbose_name=_("Genre"),
    )
    persons = models.ManyToManyField(
        Person,
        through="PersonFilmwork",
        verbose_name=_("Person"),
    )

    class Meta:
        db_table = "film_work"
        verbose_name = _("Movie")
        verbose_name_plural = _("Movies")
        indexes = [
            models.Index(
                fields=["creation_date"],
                name="film_work_creation_date_idx",
            )
        ]

    def __str__(self):
        return self.title


class GenreFilmWork(CreatedMixin, UUIDMixin):
    """Промежуточная модель связи кинопроизведений и жанров."""

    film_work = models.ForeignKey("Filmwork", on_delete=models.CASCADE)
    genre = models.ForeignKey("Genre", on_delete=models.CASCADE)

    class Meta:
        db_table = "genre_film_work"
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")
        constraints = [
            models.UniqueConstraint(
                fields=["film_work", "genre"],
                name="film_work_genre_idx",
            )
        ]


class PersonFilmWork(CreatedMixin, UUIDMixin):
    """Промежуточная модель связи кинопроизведений и персон."""

    class Role(models.TextChoices):
        """Класс вариантов выбора должности."""

        actor = "actor"
        director = "director"
        writer = "writer"

    film_work = models.ForeignKey("Filmwork", on_delete=models.CASCADE)
    person = models.ForeignKey("Person", on_delete=models.CASCADE)
    role = models.TextField(_("role"), choices=Role.choices, blank=True)

    class Meta:
        db_table = "person_film_work"
        verbose_name = _("Function")
        verbose_name_plural = _("Functions")
        constraints = [
            models.UniqueConstraint(
                fields=["film_work", "person", "role"],
                name="film_work_person_role_idx",
            )
        ]
