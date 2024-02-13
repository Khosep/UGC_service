"""Модели датаклассов для таблиц."""
from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass
class IDCreatedMixin:
    """Абстрактная модель для полей ID и created_at."""

    id: uuid4
    created_at: datetime

    class Meta:
        abstract = True


@dataclass
class UpdatedMixin:
    """Абстрактная модель для поля updated_at."""

    updated_at: datetime

    class Meta:
        abstract = True


@dataclass
class Genre(IDCreatedMixin, UpdatedMixin):
    name: str
    description: str


@dataclass
class GenreFilmWork(IDCreatedMixin):
    film_work_id: uuid4
    genre_id: uuid4


@dataclass
class PersonFilmWork(IDCreatedMixin):
    film_work_id: uuid4
    person_id: uuid4
    role: str


@dataclass
class Person(IDCreatedMixin, UpdatedMixin):
    full_name: str


@dataclass
class FilmWork(IDCreatedMixin, UpdatedMixin):
    title: str
    description: str
    creation_date: datetime
    rating: float
    type: str = field(default="movie")
