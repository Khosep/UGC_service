from datetime import datetime
from pydantic import BaseModel


class KafkaMessage(BaseModel):
    key: bytes
    value: bytes


class FilmTimestampMessage(BaseModel):
    user_id: str | None = None
    film_id: str
    film_timestamp_sec: int
    username: str | None = ''
    roles: list[str] | None = []
    email: str | None = ''
    first_name: str | None = ''
    last_name: str | None = ''
    event_time: datetime