from uuid import UUID
from pydantic import BaseModel


class FilmTimestamp(BaseModel):
    film_id: UUID
    film_timestamp_sec: int
