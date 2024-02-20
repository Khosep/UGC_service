from uuid import UUID

from schemas.mixins import (
    CreatedMixinSchema,
    IdMixinSchema,
    UserIdFilmIdMixinSchema,
)
from pydantic import BaseModel

class FilmTimestamp(BaseModel):
    film_id: UUID
    film_timestamp_sec: int

